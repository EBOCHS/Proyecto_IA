
let clasificador;
let video;

let estado;
let probabilidad;


function setup() {
    noCanvas();
    // Inicializa la camara
    video = createCapture(VIDEO);
    video.id("video");
    // Inicializa le clasificador de imagenes con el video
    clasificador = ml5.imageClassifier("MobileNet", video, modeloListo);
    
    let camaraIA = document.getElementById("video");
    let contenedorCamara = document.getElementById("contenedorCamara");
    contenedorCamara.appendChild(camaraIA);
}
    


//Cuando el modelo este listo
function modeloListo() {
    // Cambiamos el estado a Modelo cargado
    select("#estado").html("Modelo cargado");
    // Llama al la funcion para comenzar a clasificar el video
    clasificarVideo();
}
// Predecimos que imagen es la que se muestra en el video
function clasificarVideo() {
    clasificador.predict(tomaResultado);
}


// Cuando obtenemos el resultado
function tomaResultado(err, resultado) {
    
    // Escribimos el nombre de la imagen detectada
    // document.getElementById("probabilidad").addEventListener("change",()=>{
    // document.getElementById("video").style.border = "thick solid #dc143c";
    // });
   // console.log(nf(resultado[0].probability, 0, 2) > '0.85')

    if (
        resultado[0].className == "orange" &&
        nf(resultado[0].probability, 0, 2) > "0.60"
    ) {
        document.getElementById("video").style.border =
            "thick solid #00f02b";
        select("#resultado").html("Naranja en Buen Estado");
        select("#probabilidad").html(nf(resultado[0].probability, 0, 2));
        estado='Naranja en Buen estado'
        probabilidad=nf(resultado[0].probability, 0, 2);

        axios.post('/insertar-reconocimiento-fruta',{estado:estado, probabilidad:probabilidad        
        }).then(res=>{
            console.log(res.data)
        })   
    } 
     
    if (
        resultado[0].className == "orange" &&
        nf(resultado[0].probability, 0, 2) < "0.60"
    ) {
        document.getElementById("video").style.border =
            "thick solid #dc143c";
        select("#resultado").html("Naranja en Mal estado");
        select("#probabilidad").html(nf(resultado[0].probability, 0, 2));
        estado='Naranja en Mal estado'
        probabilidad=nf(resultado[0].probability, 0, 2);
            axios.post('/insertar-reconocimiento-fruta',{estado:estado, probabilidad:probabilidad        
            }).then(res=>{
                console.log(res.data)
            })
            sleep(3000)
    } else {
        document.getElementById("video").style.border =
            "thick solid #1a3bd6";
        select("#resultado").html("Identificando...");
        select("#probabilidad").html(""); 
    }
    // Llamamos de nuevo al clasificador
    
    clasificarVideo();
}
