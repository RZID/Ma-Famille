// Routes college.rzidinc.com/ma-famille/* to the prefixed Pages build.
// The Pages project is built with VITE_BASE_PATH=/ma-famille/, so asset
// URLs and the vue-router base already include the prefix — this worker
// only strips it before fetching and fixes redirect Locations on the way
// back. No HTML rewriting involved.

const PAGES_HOST = "ma-famille-path.pages.dev";
const PREFIX = "/ma-famille";

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith(PREFIX + "/") && url.pathname !== PREFIX) {
      return new Response("Not found", { status: 404 });
    }
    const rest = url.pathname.slice(PREFIX.length) || "/";
    const target = new URL(rest + url.search, `https://${PAGES_HOST}`);
    const init = {
      method: request.method,
      headers: request.headers,
      redirect: "manual",
    };
    if (request.method !== "GET" && request.method !== "HEAD") {
      init.body = request.body;
    }
    const res = await fetch(target.toString(), init);
    const location = res.headers.get("location");
    if (location) {
      const fixed = location.replace(`https://${PAGES_HOST}`, PREFIX);
      const headers = new Headers(res.headers);
      headers.set("location", fixed.startsWith("http") ? fixed : location);
      return new Response(res.body, { status: res.status, headers });
    }
    return res;
  },
};
