self.addEventListener("install", function(event) {
    console.log("AI Scanner Service Worker hazır");
});


self.addEventListener("activate", function(event) {
    console.log("AI Scanner aktif");
});


self.addEventListener("push", function(event) {

    let veri = {
        title: "🚀 BTCTürk AI Scanner",
        body: "Yeni fırsat bulundu!"
    };


    if(event.data){
        veri = event.data.json();
    }


    event.waitUntil(

        self.registration.showNotification(
            veri.title,
            {
                body: veri.body,
                icon: "/icon.png"
            }
        )

    );

});
