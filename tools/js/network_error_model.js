"use strict";

function classifyNetworkError(errorObject) {
  const networkError = errorObject?.network_error ?? errorObject ?? {};
  if (networkError.code === "ENETUNREACH") {
    return {
      category: "routing-or-connect",
      completedConnection: false,
      evidenceMeaning: "weighs against completed direct-IP transmission"
    };
  }
  if (networkError.code === "ECONNREFUSED") {
    return {
      category: "destination-refused",
      completedConnection: false,
      evidenceMeaning: "host was reachable enough to refuse the connection"
    };
  }
  return {
    category: "unknown",
    completedConnection: null,
    evidenceMeaning: "requires additional telemetry"
  };
}

module.exports = { classifyNetworkError };

