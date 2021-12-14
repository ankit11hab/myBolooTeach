var testConnectionSpeed = {
    imageAddr : "https://upload.wikimedia.org/wikipedia/commons/a/a6/Brandenburger_Tor_abends.jpg", // this is just an example, you rather want an image hosted on your server
    downloadSize : 2707459, // this must match with the image above
    run:function(mbps_max,cb_gt,cb_lt){
      testConnectionSpeed.mbps_max = mbps_max;
      testConnectionSpeed.cb_gt = cb_gt;
      testConnectionSpeed.cb_lt = cb_lt;
      testConnectionSpeed.InitiateSpeedDetection();
    },
    InitiateSpeedDetection: function() {
      window.setTimeout(testConnectionSpeed.MeasureConnectionSpeed, 1);
    },
    result:function(){
      var duration = (endTime - startTime) / 1000;
      var bitsLoaded = testConnectionSpeed.downloadSize * 8;
      var speedBps = (bitsLoaded / duration).toFixed(2);
      var speedKbps = (speedBps / 1024).toFixed(2);
      var speedMbps = parseFloat((speedKbps / 1024).toFixed(2));
      if(speedMbps >= this.mbps_max){
        testConnectionSpeed.cb_gt ? testConnectionSpeed.cb_gt(speedMbps) : false;
      }else {
        testConnectionSpeed.cb_lt ? testConnectionSpeed.cb_lt(speedMbps) : false;
      }
    },
    MeasureConnectionSpeed:function() {
      var download = new Image();
      download.onload = function () {
          endTime = (new Date()).getTime();
          testConnectionSpeed.result();
      }
      startTime = (new Date()).getTime();
      var cacheBuster = "?nnn=" + startTime;
      download.src = testConnectionSpeed.imageAddr + cacheBuster;
    }
}

function GoodInternet(mbps){
    document.querySelector('#InternetSpeed').innerHTML = mbps + 'Mbps.............. ' + '<span style="color:green"><b>Successfull<b><span>'
}

function PoorInternet(mbps){
    document.querySelector('#InternetSpeed').innerHTML = mbps + 'Mbps............... ' + '<span style="color:red"><b>Poor Internet Connection<b><span>'
}

function checkUserCamera(){
    var constraints = { audio: false, video: true };

    navigator.mediaDevices.getUserMedia(constraints)
    .then(function(mediaStream) {
        var video = document.querySelector('#camera');
        video.srcObject = mediaStream;
        document.querySelector('#webcamCheckStatus').innerHTML = '<span style="color:green"><b>Successfull<b><span>'
        video.onloadedmetadata = function(e) {
            video.play();
        };
    })
    .catch(function(err) { 
        // alert("Camera/Microphone not detected" + "\nYou will be redirected to dashboard");

        console.log(err); 
        document.querySelector('#webcamCheckStatus').innerHTML = '<span style="color:red"><b>Unsuccesfull<b><span>'
        // location.replace("{% url 'home' %}")
    }); 

}

(async () => {
    let volumeCallback = null;
    let volumeInterval = null;
    const volumeVisualizer = document.getElementById('MicrophoneResult');
    // Initialize
    try {
      const audioStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true
        }
      });
      const audioContext = new AudioContext();
      const audioSource = audioContext.createMediaStreamSource(audioStream);
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 512;
      analyser.minDecibels = -127;
      analyser.maxDecibels = 0;
      analyser.smoothingTimeConstant = 0.4;
      audioSource.connect(analyser);
      const volumes = new Uint8Array(analyser.frequencyBinCount);
      volumeCallback = () => {
        analyser.getByteFrequencyData(volumes);
        let volumeSum = 0;
        for(const volume of volumes)
          volumeSum += volume;
        const averageVolume = volumeSum / volumes.length;
        var vol = (averageVolume / 5).toString()
        volumeVisualizer.style.width = vol+'%';
        if(parseInt(vol)>20){
            volumeVisualizer.style.backgroundColor = 'green'
            document.getElementById('microphoneCheckStatus').innerHTML = "<b style='color:green;'>Successfull</b>"
        }
      };
    } catch(e) {
      console.error('Failed to initialize volume visualizer, simulating instead...', e);
      // Simulation
      //TODO remove in production!
      let lastVolume = 50;
      volumeCallback = () => {
        var volume = Math.min(Math.max(Math.random() * 100, 0.8 * lastVolume), 1.2 * lastVolume);
        volume = volume/5;
        lastVolume = volume;
        volumeVisualizer.style.width = volume.toString()+'%';
        if(parseInt(volume)>20){
            volumeVisualizer.style.backgroundColor = 'green'
            document.getElementById('microphoneCheckStatus').innerHTML = "<b style='color:green;'>Successfull</b>"
        }
      };
    }
    volumeInterval = setInterval(volumeCallback, 100);

})();

function getLocation(){
    navigator.geolocation.getCurrentPosition((cordinates)=>{
        const latitude = cordinates.coords.latitude
        const longitude = cordinates.coords.longitude
        if(latitude>=8.4 && latitude <=37.6 && longitude>=68.7 && longitude<=97.25){
            document.getElementById("LocationStatus").innerHTML = `<b style="color:green">${latitude}° N, ${longitude}° E...........INDIA</b>`
        }
        else{
            document.getElementById("LocationStatus").innerHTML = `<b style="color:red">${latitude}° N, ${longitude}° E..........Not allowed outside INDIA</b>`
        }
    }, (error)=>{
        console.log(error)
    })
}

function checkBrowser() {
          
    // Get the user-agent string
    let userAgentString = 
    navigator.userAgent;

    // Detect Chrome
    let chromeAgent = 
        userAgentString.indexOf("Chrome") > -1;

    // Detect Internet Explorer
    let IExplorerAgent = 
        userAgentString.indexOf("MSIE") > -1 || 
        userAgentString.indexOf("rv:") > -1;

    // Detect Firefox
    let firefoxAgent = 
        userAgentString.indexOf("Firefox") > -1;

    // Detect Safari
    let safariAgent = 
        userAgentString.indexOf("Safari") > -1;
        
    // Discard Safari since it also matches Chrome
    if ((chromeAgent) && (safariAgent)) 
        safariAgent = false;

    // Detect Opera
    let operaAgent = 
        userAgentString.indexOf("OP") > -1;
        
    // Discard Chrome since it also matches Opera     
    if ((chromeAgent) && (operaAgent)) 
        chromeAgent = false;

    if(chromeAgent){
        document.getElementById('browserCheckStatus').innerHTML = '<b style="color:green">Chrome</b>'
    }
    else if(firefoxAgent){
        document.getElementById('browserCheckStatus').innerHTML = '<b style="color:green">FireFox</b>'
    }
    else if(safariAgent){
        document.getElementById('browserCheckStatus').innerHTML = '<b style="color:green">Safari</b>'
    }
    else{
        document.getElementById('browserCheckStatus').innerHTML = '<b style="color:red">Browser Not Supported<br>Please Open in Chrome, FireFox or Safari</b>'
    }

}



testConnectionSpeed.run(1.5, (mbps) => GoodInternet(mbps), (mbps) => PoorInternet(mbps))
checkUserCamera()
getLocation()
checkBrowser()