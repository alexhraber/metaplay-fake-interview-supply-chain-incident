"use strict";

function buildBeaconQuery(fakeSysInfo, fakeProcessInfo, tid, sysId) {
  const url = new URL("http://127.0.0.1:9001/api/checkStatus");
  url.search = new URLSearchParams({
    sysInfo: JSON.stringify(fakeSysInfo),
    processInfo: JSON.stringify(fakeProcessInfo),
    tid: String(tid),
    sysId: String(sysId)
  }).toString();
  return url.toString();
}

function parseBeaconQuery(urlText) {
  const url = new URL(urlText);
  if (url.hostname !== "127.0.0.1") {
    throw new Error("Only loopback beacon fixtures are accepted");
  }
  return Object.fromEntries(url.searchParams.entries());
}

module.exports = { buildBeaconQuery, parseBeaconQuery };

