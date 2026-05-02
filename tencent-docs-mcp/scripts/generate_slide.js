#!/usr/bin/env node
/**
 * generate_slide.js - AI 生成 PPT 异步轮询脚本
 *
 * 腾讯文档的 create_slide 是异步接口，需要轮询 slide_progress 直到完成。
 * 本脚本封装了完整的异步流程：
 *   1. 调用 create_slide 发起生成任务
 *   2. 每 5 秒轮询 slide_progress
 *   3. 完成后输出 file_id 和 URL
 *
 * 用法：
 *   node generate_slide.js --description "用户需求描述" [--reference "参考材料"]
 */

const { execSync } = require('child_process');
const path = require('path');

const MCP_SERVICE = 'tencent-docs';
const POLL_INTERVAL = 5000; // 5秒

function mcporterCall(toolName, args) {
  const argsStr = JSON.stringify(args);
  try {
    const output = execSync(
      `mcporter call "${MCP_SERVICE}" "${toolName}" --args '${argsStr}'`,
      { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
    );
    return JSON.parse(output.trim());
  } catch (err) {
    const raw = err.stdout || err.message || '';
    // 尝试从错误输出中提取 JSON
    const match = raw.match(/\{[\s\S]*\}/);
    if (match) {
      try { return JSON.parse(match[0]); } catch (_) {}
    }
    throw new Error(`mcporter call failed: ${raw || err.message}`);
  }
}

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { description: '', reference: '' };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--description' || args[i] === '-d') {
      result.description = args[++i] || '';
    } else if (args[i] === '--reference' || args[i] === '-r') {
      result.reference = args[++i] || '';
    }
  }
  return result;
}

async function pollProgress(taskId, maxWaitMs = 600000) {
  const start = Date.now();
  let lastStatus = -1;
  while (Date.now() - start < maxWaitMs) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL));
    try {
      const res = mcporterCall('slide_progress', { task_id: taskId });
      const currentStatus = res.status;
      if (currentStatus === 2) {
        // 完成
        return res;
      }
      if (currentStatus !== lastStatus) {
        lastStatus = currentStatus;
        console.log(`  [${new Date().toLocaleTimeString()}] 状态: ${statusLabel(currentStatus)} ...`);
      }
      }
    } catch (e) {
      console.error(`  轮询出错: ${e.message}，继续等待...`);
    }
  }
  throw new Error('PPT 生成超时（10分钟）');
}

function statusLabel(status) {
  const map = {
    '-1': '失败',
    '0': '排队中',
    '1': '生成中',
    '2': '已完成',
    '3': '失败'
  };
  return map[String(status)] || `未知(${status})`;
}

async function main() {
  const { description, reference } = parseArgs();
  if (!description) {
    console.error('用法: node generate_slide.js --description "PPT需求描述" [--reference "参考材料"]');
    process.exit(1);
  }

  console.log('🚀 开始生成 PPT...');
  console.log(`📝 需求: ${description}`);
  if (reference) console.log(`📎 参考: ${reference}`);

  // 1. 发起生成任务
  console.log('\n📤 正在调用 create_slide...');
  const createArgs = { description };
  if (reference) createArgs.reference_context = reference;

  const createRes = mcporterCall('create_slide', createArgs);

  if (createRes.error) {
    console.error(`❌ 创建失败: ${createRes.error}`);
    process.exit(1);
  }

  const taskId = createRes.task_id;
  console.log(`✅ 任务已创建，task_id: ${taskId}`);
  console.log('⏳ 等待 PPT 生成完成（每 5 秒轮询）...\n');

  // 2. 轮询等待完成
  const finalRes = await pollProgress(taskId);

  console.log('\n✅ PPT 生成完成！');
  console.log(`📄 file_id: ${finalRes.file_id || createRes.file_id || 'N/A'}`);
  console.log(`🔗 URL: ${finalRes.url || createRes.url || 'N/A'}`);
  if (finalRes.title) console.log(`📌 标题: ${finalRes.title}`);
}

main().catch(e => {
  console.error(`\n❌ 错误: ${e.message}`);
  process.exit(1);
});
