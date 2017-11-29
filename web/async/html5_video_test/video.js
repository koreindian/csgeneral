var video = document.getElementById("video");

// Wait for metadata to load, so that the video duration does not produce NaNs
video.onloadedmetadata = init;

function init() {
    var seek_bar = document.getElementById("seek_bar");
    var volume_bar = document.getElementById("volume_bar");

    //Set duration (async)
    setTimeout(() => {
        document.getElementById("run_time").innerHTML = format_time(video.duration); 
    }, 500); 

    //Add listeners
    document.getElementById("play").onclick = play;
    document.getElementById("mute").onclick = mute;
    document.getElementById("fullscreen").onclick = fullscreen;
    
    volume_bar.addEventListener ("change", () => {
        var vol = volume_bar.value;
        video.volume = volume_bar.value;
        mute_btn = document.getElementById("mute");
        if (vol == 0) {
            video.muted = true;
            mute_btn.className = "glyphicon glyphicon-volume-off";
        } else {
            video.muted = false;
            mute_btn.className = "glyphicon glyphicon-volume-up";
        }
    });
    
    //Seek bar listeners
    seek_bar.addEventListener ("change", () => {
        var time = video.duration * (seek_bar.value / 100);
        video.currentTime = time;
    });
    seek_bar.addEventListener("mousedown", () => {video.pause();});
    seek_bar.addEventListener("mouseup", () => {video.play();});

    video.addEventListener("timeupdate", () => {
        var slider_pos = (100 / video.duration) * video.currentTime;
        seek_bar.value = slider_pos;
        document.getElementById("current_time").innerHTML = format_time(video.currentTime);
    });
}

//Takes time in seconds, like video.duration, and
//formats it as MM:SS
function format_time(t) {
    var mins = Math.floor(t / 60);
    var secs = Math.floor(t) % 60;
    var out = "";
    
    if (secs < 10)
        out = mins + ":0" + secs;
    else
        out = mins + ":" + secs; 
    
    return out; 
}

function play() {
    var video = document.getElementById("video");
    var play_btn = document.getElementById("play");

    if (video.paused) {
        video.play();
        play_btn.className = "glyphicon glyphicon-pause";
    }
    else {
        video.pause();
        play_btn.className = "glyphicon glyphicon-play";
    }   
}

function mute() {
    var video = document.getElementById("video");
    var mute_btn = document.getElementById("mute");
    var volume_bar = document.getElementById("volume_bar");
 
    if (video.muted) {
        mute_btn.className = "glyphicon glyphicon-volume-up";
        if (video.volume == 0) { video.volume = 1; }
        volume_bar.value = video.volume;
    } else {
        mute_btn.className = "glyphicon glyphicon-volume-off";
        volume_bar.value = 0;
    }
    
    video.muted = ! video.muted;
}

function fullscreen() {
    var video = document.getElementById("video");
    if (video.reqeustFullscreen) {
        video.requestFullscreen();  
    } else if (video.mozRequestFullScreen) {
        video.mozRequestFullScreen();
    } else if (video.webkitRequestFullscreen) {
        video.webkitRequestFullscreen();
    }
}
