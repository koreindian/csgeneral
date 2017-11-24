var video = document.getElementById("my_video");
var overlay_canvas = document.getElementById("my_canvas");
var overlay_ctx = overlay_canvas.getContext("2d");
overlay_ctx.font = "30px Arial";
overlay_ctx.fillStyle = "red";
overlay_ctx.textAlign = "center";
overlay_ctx.fillText("Hey!", overlay_canvas.width/2, overlay_canvas.height/2);
