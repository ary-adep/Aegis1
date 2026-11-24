# Next release

Apply migration 002 as written. New producers should replace `ticketRef`
with `dispatchRef` in `dispatch.queued.v1`, and new consumers should expect
`dispatchRef`. Existing serialized events are retained for thirty days.
