"use strict";

function modelImportGraph(files) {
  return Object.fromEntries(
    Object.entries(files).map(([name, model]) => [
      name,
      {
        imports: [...(model.imports ?? [])],
        topLevelEffects: [...(model.topLevelEffects ?? [])]
      }
    ])
  );
}

function traceImports(graph, start, seen = new Set()) {
  if (seen.has(start)) return [];
  seen.add(start);
  const node = graph[start] ?? { imports: [] };
  return [start, ...node.imports.flatMap((next) => traceImports(graph, next, seen))];
}

module.exports = { modelImportGraph, traceImports };

