function GetSongName() {
    const element = document.getElementsByClassName("title style-scope ytmusic-player-bar")[0]
    const name = element.text['runs'][0]['text']
    return name
}

function GetImage() {
    const element = document.getElementsByClassName("image style-scope ytmusic-player-bar")[0]
    return element['src']
}
function GetTime() {
    const element = document.getElementsByClassName("time-info style-scope ytmusic-player-bar")[0]
    return element.innerHTML.trim()
}

function GetDetails() {
    let response
    const element = document.getElementsByClassName("byline style-scope ytmusic-player-bar complex-string")
    if (element[0].getAttribute('title') == "Video will play after ad") {
        response = {
            ad: true
        }
    } else {
        const info_json = element[0].text['runs']
        response = {
            ad: false,
            song: GetSongName(),
            time: GetTime(),
            image: GetImage(),
            url: window.location.href,
            artist: info_json[0].text,
            album: info_json[2].text,
            year: info_json[4].text,
        }
    }
    
    return response
}


GetDetails()