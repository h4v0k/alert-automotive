// Gallery source: the shop's Google Drive folder.
// 1) Share the folder: "Anyone with the link" → Viewer.
// 2) folderId = the long ID at the end of the folder's share link.
// 3) apiKey = a Google Cloud API key with ONLY the Google Drive API enabled,
//    restricted to HTTP referrers of this site's domain(s). Safe to be public when restricted.
window.GALLERY_CONFIG = {
  folderId: "",
  apiKey: "",
};
