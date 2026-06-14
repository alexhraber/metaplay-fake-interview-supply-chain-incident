"use strict";

function describeStagedLoader({ requestFields = [], responseBehaviors = [] } = {}) {
  return {
    loader: {
      sends: [...requestFields],
      acceptsExecutableCode: false
    },
    safeResponse: {
      type: "application/json",
      executable: false,
      behaviors: [...responseBehaviors]
    }
  };
}

function validateSafeStageDescription(response) {
  return Boolean(
    response &&
    response.type === "application/json" &&
    response.executable === false &&
    Array.isArray(response.behaviors)
  );
}

module.exports = { describeStagedLoader, validateSafeStageDescription };

