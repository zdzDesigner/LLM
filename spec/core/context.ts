import fs from "fs-extra";
import path from "path";

// 始终基于命令行运行的当前工作目录
const ROOT = process.cwd();
const SPEC_DIR = path.join(ROOT, ".spec");

export async function loadConstitution() {
  const filePath = path.join(SPEC_DIR, "memory", "constitution.md");
  if (await fs.pathExists(filePath)) {
    return await fs.readFile(filePath, "utf-8");
  }
  // 如果不存在，返回一个带有占位符的默认字符串，或者返回空字符串
  return "# Project Constitution\n> 暂无项目章程，请先运行 init。";
}

export async function loadTemplate(templateName) {
  const filePath = path.join(SPEC_DIR, "templates", templateName);
  // 简单的默认模板逻辑
  const defaultTemplate = `# Feature Specification\n\n## Context\n{{CONTEXT}}\n\n## Requirements\n{{USER_INPUT}}`;
  return (await fs.pathExists(filePath))
    ? await fs.readFile(filePath, "utf-8")
    : defaultTemplate;
}

export async function saveSpec(featureName, content) {
  const dir = path.join(SPEC_DIR, "specs", featureName);
  await fs.ensureDir(dir);
  const filePath = path.join(dir, "spec.md");
  await fs.writeFile(filePath, content);
  return dir;
}

export async function saveConstitution(content) {
  const dir = path.join(SPEC_DIR, "memory");
  await fs.ensureDir(dir);
  const filePath = path.join(dir, "constitution.md");
  await fs.writeFile(filePath, content);
  return filePath;
}
