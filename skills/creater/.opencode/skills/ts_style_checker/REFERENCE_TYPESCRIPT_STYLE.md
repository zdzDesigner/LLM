# REFERENCE_TYPESCRIPT_STYLE.md - TypeScript 规范完整文档

## 命名规范

在本项目中，严格遵守此命名规范:

1. 变量使用蛇形命名（snake_case）
2. 函数和方法使用标准的驼峰命名（camelCase）

### 变量命名规则
- **基本规则**: 使用蛇形命名法（snake_case），单词间用下划线 `_` 分隔
- **特殊情况**: 对于布尔类型的标志变量（如 `is_ready`, `has_data`），如果单词较短且语义清晰，可以省略下划线连接在一起（如 `isready`, `hasdata`）
- **多词组**: 当变量名包含多个词组时，必须使用 `_` 分隔

正确模式：
```typescript
// 基本变量命名
const hid_device = null
const device_info = {}
const polling_interval = 1000

// 布尔标志变量（短单词可以连接）
const isready = true
const hasdata = false

// 多词组变量（必须使用下划线）
const isready_update = false
const previous_devices = new Map()
```

### 函数和方法命名规则
- **基本规则**: 使用标准的驼峰命名法（camelCase），首字母小写，后续单词首字母大写
- **参数命名**: 函数参数也使用驼峰命名法

正确模式：
```typescript
// 函数命名
const calculateChecksum = (data: Buffer): number => { ... }
const packProtocolData = (type: number, data: Buffer): Buffer => { ... }

// 方法命名
interface HIDDeviceManager {
  listDevices(): Promise<HIDDeviceInfo[]>
  connect(config: HIDConfig): Promise<boolean>
  getDeviceInfo(): Promise<Device | null>
}
```

---

## Interface 与 Type 的使用规范

在本项目中，严格遵循以下 TypeScript 类型定义规范：

### Interface 的使用场景
1. **定义方法契约** - 只包含方法签名，不包含属性实现
   ```typescript
   // 正确：定义方法契约
   interface ProtocolerMethods {
     destroy(): void
     request(request: string, payload?: any): Promise<any>
     notify(notify: string, payload: any): void
   }
   ```

2. **定义函数签名** - 定义函数的参数和返回值类型
   ```typescript
   // 正确：定义函数签名
   interface FetchInitDataMethod {
     (mqtter: Protocoler, deviceInfo: DeviceData): Promise<DeviceData>
   }
   ```

### Type 的使用场景
1. **定义数据结构** - 定义对象的属性结构
   ```typescript
   // 正确：定义数据结构
   type DeviceData = {
     host: string
     ip?: string
     [key: string]: any
   }
   ```

2. **组合类型** - 组合多个接口和类型创建新的复合类型
   ```typescript
   // 正确：组合类型
   type Protocoler = ProtocolerMethods & Emitter<any>
   ```

3. **联合类型和交叉类型** - 定义复杂的类型关系
   ```typescript
   // 正确：联合类型
   type Status = 'idle' | 'recording' | 'testing'
   
   // 正确：交叉类型组合
   type ExtendedDevice = DeviceProperties & DeviceMethods
   ```

### 规范原则总结
1. **Interface 只定义方法** - Interface 应该专注于定义"能做什么"的方法契约
2. **Type 定义属性和组合** - Type 应该专注于定义"是什么"的数据结构和类型组合
3. **职责分离** - 明确区分方法定义和属性定义的职责
4. **组合优于继承** - 使用 `&` 操作符组合多种类型，而不是传统的继承
5. **函数接口与实现分离** - 使用 Interface 定义函数签名，使用具体的实现函数配合类型注解

### 参考示例
参考文件：`/packages/konvajs/src/view/design/stage/vroom/device.ts`

正确模式：
```typescript
// 方法契约定义
interface Devicer extends Selecter {
  initPos: () => { x: number; y: number }
  pos: (args?: Point) => Point | undefined
  // ... 其他方法
}

// 属性定义和类型组合
type Device = {
  type: TrKind
  node: Konva.Image
  group: Konva.Group
} & Devicer
```

这种规范使代码具有更好的类型安全性、可读性和可维护性。

---

## 代码简化策略 - 从复杂到简洁

### 大模型视角：为什么需要简化？

作为大模型，在分析代码时，我们倾向于追求：
- **单一职责**：一个函数只做一件事
- **直观调用**：API 设计符合直觉
- **最小抽象**：避免不必要的抽象层
- **可预测性**：函数行为容易理解和预测

当代码变得过于复杂时，大模型会：
1. 难以追踪调用链
2. 混淆不同职责的边界
3. 产生不确定的行为推断
4. 增加理解和维护成本

### 简化原则：3个核心思路

#### 1. 函数职责最小化
**Before**: 一个"万能"管理器处理所有事情
```typescript
// 复杂的工厂函数，职责太多
const manager = createHIDDeviceManager() // 发现+连接+通信+事件
await manager.connect(config)            // 连接设备
await manager.read()                     // 读数据
await manager.write(data)               // 写数据
const protocoler = manager.getProtocoler() // 还要创建协议处理器
```

**After**: 每个函数只负责一件事
```typescript
// 简化的独立函数，各司其职
const discover = createHIDDeviceDiscover()  // 只负责发现
const device = await hidAsyncOpen(config)   // 只负责连接
const protocoler = createProtocoler(device) // 只负责协议
```

#### 2. 直接返回 vs 工厂封装
**Before**: 工厂函数返回配置复杂的对象
```typescript
function createHIDDevice(): HIDDevice {
  // 复杂的闭包封装
  let device: HIDAsync | null = null
  const emitter = mitt<...>()
  // ...大量私有状态和方法

  return {
    connect: async (config) => { /* 复杂逻辑 */ },
    read: async () => { /* 复杂逻辑 */ },
    write: async (data) => { /* 复杂逻辑 */ },
    // ...很多方法
  }
}
```

**After**: 简单函数直接返回结果
```typescript
function hidAsyncOpen(config: HIDConfig): Promise<HIDAsync | null> {
  // 直接返回 HIDAsync 实例，无封装
  if (config.path) {
    return HIDAsync.open(config.path, { nonExclusive: true })
  }
  if (config.vendorId && config.productId) {
    return HIDAsync.open(config.vendorId, config.productId, { nonExclusive: true })
  }
  return null
}
```

#### 3. 组合调用 vs 统一接口
**Before**: 通过一个接口访问所有功能
```typescript
const manager = createHIDDeviceManager()
manager.startDiscover()     // 发现设备
await manager.connect()     // 连接设备
await manager.write(data)   // 发送数据
manager.on('data', ...)     // 监听数据
```

**After**: 按需组合独立功能
```typescript
// 需要发现时
const discover = createHIDDeviceDiscover()
discover.startDiscover()

// 需要通信时
const device = await hidAsyncOpen(config)
const protocoler = createProtocoler(device)
await protocoler.request(type, data)
```

### 简化执行步骤

#### 步骤1: 识别职责混乱
- 找到职责过多的类/函数
- 检查是否违反"单一职责原则"
- 大模型提示：如果一个函数的注释很长，可能职责太多

#### 步骤2: 职责分离
- 将复杂函数拆分为多个简单函数
- 每个函数只做一件事，且做得好
- 大模型思考：这个函数的"why"是什么？如果有多个why，就需要拆分

#### 步骤3: 移除不必要抽象
- 去掉过度设计的工厂函数
- 用直接函数调用替代复杂的对象创建
- 大模型判断：用户是否真的需要这个抽象层？

#### 步骤4: 简化接口设计
- 接口方法数量控制在5个以内
- 方法名要直观，一看就懂是做什么的
- 大模型验证：接口是否符合"最小惊讶原则"？

#### 步骤5: 验证简化效果
- 代码行数减少50%以上
- API 调用更直观
- 单元测试更容易写
- 大模型确认：简化后的代码是否更容易理解？

### 实际案例：HID 设备管理器简化

#### 复杂版本的问题：
```
createHIDDeviceManager() 返回包含15+方法的复杂对象
- 发现设备 + 连接设备 + 数据读写 + 协议处理
- 单个接口承担太多职责
- 调用链复杂，难以理解
```

#### 简化版本的优势：
```
三个独立函数，各司其职：
- createHIDDeviceDiscover() - 只负责发现
- hidAsyncOpen() - 只负责连接
- createProtocoler() - 只负责协议

使用时按需组合，大模型一看就懂
```

### 大模型友好的简化指标

✅ **好**的简化：
- 函数名就是它做的事：`hidAsyncOpen()` 打开设备，`createProtocoler()` 创建协议处理器
- 调用链短：最多2-3层调用
- 错误处理简单：每个函数只处理自己的错误
- 测试容易：每个函数独立测试

❌ **不好**的简化：
- 过度简化导致功能缺失
- 简单到没有必要的抽象
- 忽略错误处理和边界情况
- 违反既有代码的约定

### 总结：简化的艺术

代码简化不是追求"最少代码"，而是追求"最容易理解"。大模型在处理简化代码时：

1. **更容易推理**：函数行为更可预测
2. **更快理解**：职责清晰，无需深入追踪
3. **更好维护**：修改一个函数不影响其他功能
4. **更易扩展**：新功能可以独立添加

记住：**复杂不是能力，简单才是力量**。让代码像说话一样自然，让大模型像读文章一样轻松。

---

## 快速检查清单

### 命名规范检查
| 类型 | 规范 | 正确示例 | 错误示例 |
|------|------|----------|----------|
| 变量 | snake_case | `device_info` | `deviceInfo` |
| 短布尔变量 | 可连写 | `isready` | - |
| 多词变量 | 必须下划线 | `is_ready_update` | `isreadyupdate` |
| 函数 | camelCase | `calculateChecksum` | `calculate_checksum` |
| 方法 | camelCase | `getDeviceInfo` | `get_device_info` |

### Interface/Type 检查
| 场景 | 使用 | 示例 |
|------|------|------|
| 方法契约 | Interface | `interface Foo { bar(): void }` |
| 函数签名 | Interface | `interface Handler { (x: T): R }` |
| 数据结构 | Type | `type Data = { id: string }` |
| 类型组合 | Type | `type Combined = A & B` |
| 联合类型 | Type | `type Status = 'a' \| 'b'` |

### 代码简化检查
| 指标 | 警告阈值 | 建议 |
|------|----------|------|
| 函数行数 | >50行 | 拆分为多个函数 |
| 接口方法数 | >5个 | 考虑职责分离 |
| 工厂返回方法数 | >5个 | 改用组合模式 |
| 调用链深度 | >3层 | 简化抽象层次 |
