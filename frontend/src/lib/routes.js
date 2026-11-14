export function filterAndSortRoutes(routes, {
  origin = "",
  destination = "",
  query = "",
  sort = "fastest",
} = {}) {
  const search = String(query).trim().toLocaleLowerCase();
  return [...routes]
    .filter((route) => {
      const matchesOrigin = !origin || route.origin === origin;
      const matchesDestination = !destination || route.destination === destination;
      const stops = Array.isArray(route.stops) ? route.stops : [];
      const haystack = [route.name, route.origin, route.destination, ...stops]
        .filter(Boolean)
        .join(" ")
        .toLocaleLowerCase();
      return matchesOrigin && matchesDestination && haystack.includes(search);
    })
    .sort((a, b) => {
      if (sort === "frequency") {
        return a.frequency_min - b.frequency_min || a.duration_min - b.duration_min;
      }
      return a.duration_min - b.duration_min || a.name.localeCompare(b.name);
    });
}
