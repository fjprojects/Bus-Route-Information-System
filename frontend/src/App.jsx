import { useEffect, useMemo, useState } from "react";
import { getJson } from "./lib/api.js";
import { filterAndSortRoutes } from "./lib/routes.js";

const initials = (name = "") => name.split(/\s+/).map((part) => part[0]).join("").slice(0, 2).toUpperCase();

function uniqueSorted(values = []) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

export default function App() {
  const [routes, setRoutes] = useState([]);
  const [network, setNetwork] = useState({ origins: [], destinations: [], locations: [] });
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("duration");
  const [order, setOrder] = useState("asc");
  const [selectedId, setSelectedId] = useState("");
  const [selectedDetail, setSelectedDetail] = useState(null);
  const [detailStatus, setDetailStatus] = useState("idle");

  async function loadRoutes() {
    setStatus("loading");
    setError("");
    try {
      const [health, data, locationData] = await Promise.all([
        getJson("/api/health/"),
        getJson("/api/routes/?page_size=100"),
        getJson("/api/routes/locations/").catch(() => null),
      ]);
      if (health.status !== "ok") throw new Error("The route API health check did not pass.");

      const items = Array.isArray(data.items) ? data.items : [];
      const origins = locationData?.origins ?? items.map((route) => route.origin);
      const destinations = locationData?.destinations ?? items.map((route) => route.destination);
      const locations = locationData?.locations ?? items.flatMap((route) => [
        route.origin, route.destination, ...(Array.isArray(route.stops) ? route.stops : []),
      ]);

      setRoutes(items);
      setNetwork({
        origins: uniqueSorted(origins),
        destinations: uniqueSorted(destinations),
        locations: uniqueSorted(locations),
      });
      setSelectedId((current) => items.some((route) => route.id === current) ? current : items[0]?.id ?? "");
      setStatus("ready");
    } catch (err) {
      setError(err.message || "Unable to load route information.");
      setStatus("error");
    }
  }

  useEffect(() => { loadRoutes(); }, []);

  const visibleRoutes = useMemo(
    () => filterAndSortRoutes(routes, { origin, destination, query, sort, order }),
    [routes, origin, destination, query, sort, order],
  );
  const selectedRoute = visibleRoutes.find((route) => route.id === selectedId) ?? visibleRoutes[0] ?? null;

  useEffect(() => {
    if (!selectedRoute?.id) {
      setSelectedDetail(null);
      setDetailStatus("idle");
      return undefined;
    }
    let active = true;
    const fallback = selectedRoute;
    setSelectedDetail(fallback);
    setDetailStatus("loading");
    getJson(`/api/routes/${encodeURIComponent(selectedRoute.id)}/`)
      .then((payload) => {
        if (active && payload.item?.id === selectedRoute.id) {
          setSelectedDetail(payload.item);
          setDetailStatus("ready");
        }
      })
      .catch(() => {
        if (active) {
          setSelectedDetail(fallback);
          setDetailStatus("fallback");
        }
      });
    return () => { active = false; };
  }, [selectedRoute?.id]);

  const detail = selectedDetail?.id === selectedRoute?.id ? selectedDetail : selectedRoute;
  const averageDuration = routes.length
    ? Math.round(routes.reduce((sum, route) => sum + Number(route.duration_min || 0), 0) / routes.length)
    : 0;
  const fastest = [...routes].sort((a, b) => Number(a.duration_min) - Number(b.duration_min))[0];

  function clearFilters() {
    setOrigin("");
    setDestination("");
    setQuery("");
    setSort("duration");
    setOrder("asc");
  }

  return (
    <main className="app-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="Wayfinder home">
          <span className="brand-symbol">↗</span>
          <span>wayfinder<span className="brand-sub"> / transit intelligence</span></span>
        </a>
        <div className="header-right">
          <span className={`system-status ${status}`}><i />{status === "ready" ? "API connected" : status === "loading" ? "Connecting" : "API unavailable"}</span>
          <a className="header-link" href="/prototype.html" target="_blank" rel="noreferrer">Original prototype ↗</a>
        </div>
      </header>

      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">PUBLIC TRANSPORT · ROUTE DISCOVERY</p>
          <h1>Make every connection<br /><em>feel effortless.</em></h1>
          <p className="hero-description">A clearer way to explore route options, compare journey times and understand the stops between here and there.</p>
          <div className="hero-foot"><span className="pulse-dot" /> Connected to the Wayfinder Django API</div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="orbit orbit-one" /><div className="orbit orbit-two" />
          <div className="route-node node-a">A</div><div className="route-node node-b">B</div>
          <div className="route-path"><span /><span /><span /><span /></div>
          <div className="hero-art-label">YOUR CITY, CONNECTED</div>
        </div>
      </section>

      <section className="planner-card" aria-label="Route planner">
        <div className="planner-heading">
          <div><p className="eyebrow">PLAN A JOURNEY</p><h2>Where would you like to go?</h2></div>
          <span className="sample-label">DEMO NETWORK</span>
        </div>
        <form className="planner-form" onSubmit={(event) => event.preventDefault()}>
          <label className="field"><span>FROM</span><select value={origin} onChange={(event) => setOrigin(event.target.value)}><option value="">Any starting point</option>{network.origins.map((item) => <option key={item}>{item}</option>)}</select></label>
          <span className="swap-mark" aria-hidden="true">→</span>
          <label className="field"><span>TO</span><select value={destination} onChange={(event) => setDestination(event.target.value)}><option value="">Any destination</option>{network.destinations.map((item) => <option key={item}>{item}</option>)}</select></label>
          <button className="primary-button" type="submit">Explore routes <span>↗</span></button>
        </form>
        <div className="network-meta"><span>{network.locations.length} sample locations</span><span>·</span><span>Origins, destinations and intermediate stops indexed</span></div>
      </section>

      <section className="metrics-row" aria-label="Network overview">
        <article className="metric"><span className="metric-icon">⌁</span><div><strong>{routes.length.toString().padStart(2, "0")}</strong><small>Sample routes</small></div></article>
        <article className="metric"><span className="metric-icon">◷</span><div><strong>{averageDuration}<small> min</small></strong><small>Average sample journey</small></div></article>
        <article className="metric"><span className="metric-icon">✦</span><div><strong>{fastest ? fastest.duration_min : "—"}<small> min</small></strong><small>Fastest sample route</small></div></article>
        <article className="metric metric-note"><span className="live-indicator" /> <div><strong>Sample data</strong><small>No live operator feed connected</small></div></article>
      </section>

      <section className="workspace">
        <div className="results-column">
          <div className="section-heading">
            <div><p className="eyebrow">ROUTE EXPLORER</p><h2>Available connections <span>{visibleRoutes.length}</span></h2></div>
            <div className="route-controls">
              <label className="sort-control"><span>SORT BY</span><select value={sort} onChange={(event) => setSort(event.target.value)}><option value="duration">Shortest journey</option><option value="frequency">Most frequent</option><option value="name">Route name</option></select></label>
              <label className="sort-control"><span>ORDER</span><select value={order} onChange={(event) => setOrder(event.target.value)}><option value="asc">Ascending</option><option value="desc">Descending</option></select></label>
            </div>
          </div>
          <div className="search-box"><span>⌕</span><input list="wayfinder-locations" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search routes, stops or places…" aria-label="Search routes and stops" /><datalist id="wayfinder-locations">{network.locations.map((item) => <option key={item} value={item} />)}</datalist>{query && <button onClick={() => setQuery("")} aria-label="Clear search" type="button">×</button>}</div>
          <div className="results-actions"><span>Showing {visibleRoutes.length} of {routes.length} routes</span><button className="text-button" type="button" onClick={clearFilters}>Reset planner</button></div>
          {status === "loading" && <div className="state-card">Loading route information…</div>}
          {status === "error" && <div className="state-card error-state"><strong>We could not reach the route service.</strong><p>{error}</p><button className="outline-button" onClick={loadRoutes}>Try again</button></div>}
          {status === "ready" && visibleRoutes.length === 0 && <div className="state-card"><strong>No matching routes</strong><p>Try a different origin, destination or search term.</p><button className="text-button" onClick={clearFilters}>Clear filters</button></div>}
          <div className="route-list">
            {visibleRoutes.map((route, index) => (
              <button className={`route-card ${selectedRoute?.id === route.id ? "selected" : ""}`} key={route.id} onClick={() => setSelectedId(route.id)} aria-pressed={selectedRoute?.id === route.id}>
                <div className="route-card-top"><div className="route-name-wrap"><span className={`route-avatar route-${index % 3}`}>{initials(route.name)}</span><div><strong>{route.name}</strong><small>{route.origin} to {route.destination}</small></div></div><div className="duration"><strong>{route.duration_min}</strong><small>MINUTES</small></div></div>
                <div className="stop-preview">{(route.stops ?? []).map((stop, stopIndex) => <span className="stop-chip" key={stop + stopIndex}>{stop}</span>)}</div>
                <div className="route-card-bottom"><span>◷ Every {route.frequency_min} min <small>· sample frequency</small></span><span className="details-link">View details ↗</span></div>
              </button>
            ))}
          </div>
        </div>

        <aside className="detail-panel">
          <div className="detail-panel-head"><p className="eyebrow">JOURNEY DETAILS</p><span className="detail-badge">{detailStatus === "loading" ? "LOADING" : "PREVIEW"}</span></div>
          {detail ? <>
            <h3>{detail.name}</h3><p className="detail-subtitle">A sample connection across the demo network.</p>
            <div className="journey-summary"><div><small>ESTIMATED TIME</small><strong>{detail.duration_min}<span> min</span></strong></div><div><small>FREQUENCY</small><strong>{detail.frequency_min}<span> min</span></strong></div></div>
            <div className="timeline-title">YOUR STOP SEQUENCE <span>{detail.stops?.length ?? 0} STOPS</span></div>
            <div className="timeline">{(detail.stops ?? []).map((stop, index) => <div className="timeline-stop" key={stop + index}><span className={index === 0 || index === detail.stops.length - 1 ? "timeline-dot endpoint" : "timeline-dot"} /><div><strong>{stop}</strong><small>{index === 0 ? "Starting point" : index === detail.stops.length - 1 ? "Destination" : "Along the route"}</small></div></div>)}</div>
            <p className="detail-service">{detail.service_label || "Illustrative sample service"}</p>
          </> : <div className="empty-detail">Select a route to inspect its stops.</div>}
          <div className="detail-disclaimer"><strong>Prototype notice</strong><p>Stops, timings and service frequencies are illustrative. Confirm actual services with the relevant transport operator.</p></div>
        </aside>
      </section>
      <footer className="site-footer"><span>WAYFINDER <i>·</i> ROUTE DISCOVERY PLATFORM</span><span>Built with React + Django <b>·</b> Sample network only</span></footer>
    </main>
  );
}
