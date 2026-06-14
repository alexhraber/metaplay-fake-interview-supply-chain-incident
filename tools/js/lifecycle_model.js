"use strict";

const LIFECYCLE_NAMES = new Set([
  "preinstall", "install", "postinstall", "prepare"
]);
const SUSPICIOUS_TOKENS = [
  "nohup", "start /b", "node server", "curl", "wget", "powershell", "&"
];

function parseLifecycleScripts(packageJson) {
  const scripts = packageJson?.scripts ?? {};
  return Object.entries(scripts)
    .filter(([name]) => LIFECYCLE_NAMES.has(name))
    .map(([name, command]) => ({ name, command: String(command) }));
}

function findSuspiciousLifecycleScripts(packageJson) {
  return parseLifecycleScripts(packageJson).flatMap(({ name, command }) => {
    const normalized = command.toLowerCase();
    return SUSPICIOUS_TOKENS
      .filter((token) => normalized.includes(token))
      .map((token) => ({ name, command, matchedToken: token }));
  });
}

module.exports = { parseLifecycleScripts, findSuspiciousLifecycleScripts };

