function searchStations() {
    let location = document.getElementById("location").value;
    
    fetch(`/stations?location=${location}`)
    .then(response => response.json())
    .then(data => {
        let stationsDiv = document.getElementById("stations");
        stationsDiv.innerHTML = "";
        data.stations.forEach(station => {
            stationsDiv.innerHTML += `<p>${station.name} - ${station.address} 
                <button onclick="bookStation(${station.id})">Book Now</button></p>`;
        });
    });
}

function bookStation(stationId) {
    fetch(`/book/${stationId}`, { method: "POST" })
    .then(response => response.json())
    .then(data => alert(data.message));
}
