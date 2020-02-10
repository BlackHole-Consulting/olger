var ShodanClient = require('shodan-api');
var client = new ShodanClient({ key: '' });
var fs = require('fs');

var query = process.argv[2]+" "+ process.argv[3]

console.log(client);
function getlist (pagina){

  const searchOpts = {
      minify: true,
      page: pagina,
      timeout: 100000
  };

  client.search(query, searchOpts, function (err, response) {
    var ret = JSON.stringify(response)
    console.log(query);
    console.log(response.length);
    var parsedResponse = JSON.parse(ret);
    console.log(parsedResponse);
    if(parsedResponse!==null){
      console.log(parsedResponse);
      if(!parsedResponse.error && parsedResponse["matches"]){
      console.log(parsedResponse["matches"].length);
        for(var i = 0; i < parsedResponse["matches"].length;i++){
          var dt = JSON.stringify(parsedResponse["matches"][i]);
          var ip = parsedResponse["matches"][i]["ip_str"];
          var port = parsedResponse["matches"][i]["port"]; 
        	save(dt,ip,port);
        }
        console.log((pagina*100));
        if((pagina*100)< parsedResponse["total"]){
          pagina++;
          getlist(pagina);
        }
      }else{
        setTimeout(function(){ getlist(pagina); }, 3000);
        
      }  
    }else{
      setTimeout(function(){ getlist(pagina); }, 3000);
    }
    
  });
}
 


function save(data,ip,port) {
    try {
      //raw json
      //fs.appendFileSync("lists/"+ip+".hole", data);
      fs.appendFileSync("lists/"+query,ip+","+port+"\n")
    } catch (err) {
      /* Handle the error */
    }
 }

 getlist(1);
