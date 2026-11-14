import test from "node:test";
import assert from "node:assert/strict";
import { filterAndSortRoutes, toggleComparedRoute } from "../src/lib/routes.js";

const routes = [
  { id: "blue", name: "Blue Line", origin: "Central Station", destination: "Tech Park", stops: ["Market Square"], duration_min: 22, frequency_min: 12 },
  { id: "green", name: "Green Line", origin: "Central Station", destination: "University", stops: ["Museum"], duration_min: 16, frequency_min: 15 },
  { id: "orange", name: "Orange Line", origin: "Riverside", destination: "Tech Park", stops: ["Market Square"], duration_min: 25, frequency_min: 18 },
];

test("filters by origin and destination without case sensitivity", () => {
  assert.deepEqual(filterAndSortRoutes(routes, { origin: "central station", destination: "TECH PARK" }).map((r) => r.id), ["blue"]);
});

test("search includes intermediate stops and route identifiers", () => {
  assert.deepEqual(filterAndSortRoutes(routes, { query: "museum" }).map((r) => r.id), ["green"]);
  assert.deepEqual(filterAndSortRoutes(routes, { query: "ORANGE" }).map((r) => r.id), ["orange"]);
});

test("sorts by frequency when requested", () => {
  assert.deepEqual(filterAndSortRoutes(routes, { sort: "frequency" }).map((r) => r.id), ["blue", "green", "orange"]);
});

test("supports descending numeric and alphabetical order", () => {
  assert.deepEqual(filterAndSortRoutes(routes, { sort: "duration", order: "desc" }).map((r) => r.id), ["orange", "blue", "green"]);
  assert.deepEqual(filterAndSortRoutes(routes, { sort: "name" }).map((r) => r.id), ["blue", "green", "orange"]);
});

test("does not mutate the source array", () => {
  const copy = [...routes];
  filterAndSortRoutes(routes, { sort: "fastest" });
  assert.deepEqual(routes, copy);
});

test("empty filters return all routes, fastest first", () => {
  assert.deepEqual(filterAndSortRoutes(routes).map((r) => r.id), ["green", "blue", "orange"]);
});


test("route comparison toggles IDs and enforces a maximum of three", () => {
  const first = toggleComparedRoute([], "blue");
  const second = toggleComparedRoute(first, "green");
  const third = toggleComparedRoute(second, "orange");
  assert.deepEqual(third, ["blue", "green", "orange"]);
  assert.deepEqual(toggleComparedRoute(third, "purple"), third);
  assert.deepEqual(toggleComparedRoute(third, "green"), ["blue", "orange"]);
  assert.deepEqual(first, ["blue"]);
});
