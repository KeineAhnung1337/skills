# SWT / JFace correctness before micro-optimization

SWT controls are bound to the creating `Display`'s UI thread. Never read or mutate widget state from a background job; use the appropriate display scheduling method and re-check `isDisposed()` when execution occurs. Do not block the UI thread waiting for the job that needs the UI thread. Keep event handlers and paint callbacks short; cache measured expensive work without creating stale state.

Widget parents normally dispose child widgets, but native resources (such as images, colors, fonts, cursors, and GCs) can have different ownership rules. Consult the specific 4.40 Javadoc and platform resource manager (`JFaceResources`, local resource managers) before disposing or caching anything; do not dispose shared/system resources. Remove listeners and unsubscribe when their owner ends; cancel delayed UI callbacks and jobs on view/part shutdown where applicable.

For large viewers, inspect the content provider, filters, label provider, sorting, refresh frequency, and synchronous model traversal. Reduce unnecessary full `refresh()` calls, use batching/deltas if supported, and verify selection preservation. For charts/tables/images measure paint/update and per-row allocation; do not cache `GC` or widgets beyond their lifecycle.

Offline docs: `guide/swt.htm`, `guide/swt_threading.htm`, `guide/swt_graphics.htm`, `guide/jface_viewers.htm`, `reference/api/org/eclipse/swt/`, `reference/api/org/eclipse/jface/`. Compare behavior on the supported host OS/display stack because SWT is native-backed.
