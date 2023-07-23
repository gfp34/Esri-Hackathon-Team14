require(["esri/config",
 "esri/WebMap", 
 "esri/views/MapView", 
 "esri/widgets/Search",
 "esri/widgets/LayerList",
 "esri/widgets/Legend"],
 function(esriConfig, WebMap, MapView, Search, LayerList) {
  
  esriConfig.apiKey = "AAPK213e574c6f914df48c957612cb5a80d2BdiE6IixjuztBRUskTn8Ks31dp_WWCqkL1TBs_6HBIwzXgcVXgofZaCot7_tys4q";
  let myJSON = {workAddr1: "", workAddr2: ""}
  
  const webmap = new WebMap({
      portalItem: {
          id: "65d6edb51a034bbc975bd9b1a10e221f"
      }
  });

  const view = new MapView({
      map: webmap,
      container: "viewDiv",
  });
  
  const workSearch = new Search({  //Add Search widget
    view: view,
    includeDefaultSources: false,
    sources: [
      {
        url: "https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer",
        singleLineFieldName: "SingleLine",
        outFields: ["Addr_type"],
        name: "Geocoder",
        placeholder: "Enter Work Address",
      }
    ],
  });

  const logoSvg = document.createElement("img");
  logoSvg.src = "/FullLogo.svg"
  view.ui.add(logoSvg, "top-right");
  view.ui.add(workSearch, "top-right"); //Add to the map

  workSearch.on("select-result", function(event){
    console.log("The selected search result: ", event.result.name);
    myJSON.workAddr1 = event.result.name;
    console.log(JSON.stringify(myJSON));
  });

  
  view.when(() => {
    const layerList = new LayerList({
      view: view
    });

    // Add widget to the top right corner of the view
    view.ui.add(layerList, "bottom-right");
  });

  
});
