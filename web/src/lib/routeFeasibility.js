// Picks the row of the fixed route-feasibility report to show. Pure, so it can be tested without React.
// An exact match on the current roughness and confidence wins; otherwise the report's headline row is used.
export function pickRow(data, params) {
  if (!data || !Array.isArray(data.rows) || !data.headline) return null;
  const match = data.rows.find((r) => r.roughness === params?.roughness && r.confidence === params?.confidence);
  if (match) return { row: match, exact: true };
  const head = data.rows.find(
    (r) => r.roughness === data.headline.roughness && r.confidence === data.headline.confidence
  );
  return head ? { row: head, exact: false } : null;
}
