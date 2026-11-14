const normalize = (value) => String(value ?? "").trim().toLocaleLowerCase();

export function filterAndSortRoutes(routes, {
  origin = "",
  destination = "",
  query = "",
  sort = "duration",
  order = "asc",
} = {}) {
  const search = normalize(query);
  const normalizedOrigin = normalize(origin);
  const normalizedDestination = normalize(destination);

  const matched = routes.filter((route) => {
    const matchesOrigin = !normalizedOrigin || normalize(route.origin) === normalizedOrigin;
    const matchesDestination = !normalizedDestination || normalize(route.destination) === normalizedDestination;
    const stops = Array.isArray(route.stops) ? route.stops : [];
    const searchable = [route.name, route.id, route.origin, route.destination, ...stops]
      .filter(Boolean)
      .map(normalize)
      .join(" ");

    return matchesOrigin && matchesDestination && (!search || searchable.includes(search));
  });

  const sortFields = {
    fastest: "duration_min",
    duration: "duration_min",
    frequency: "frequency_min",
    name: "name",
  };
  const field = sortFields[sort] ?? sortFields.duration;
  const direction = order === "desc" ? -1 : 1;

  return matched.sort((left, right) => {
    const a = left[field];
    const b = right[field];
    const comparison = field === "name"
      ? String(a ?? "").localeCompare(String(b ?? ""), undefined, { sensitivity: "base" })
      : Number(a ?? 0) - Number(b ?? 0);
    return comparison * direction || String(left.name ?? "").localeCompare(String(right.name ?? ""));
  });
}


export function toggleComparedRoute(ids = [], routeId, limit = 3) {
  if (!routeId) return ids;
  if (ids.includes(routeId)) return ids.filter((id) => id !== routeId);
  if (ids.length >= limit) return ids;
  return [...ids, routeId];
}
