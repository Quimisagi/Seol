export function confirmar_pago(){
  console.log("ENTRA CONFIRMAR PAGO");
  var data = {}

  var numero = document.querySelector('#numero_0').value;

  var fecha = document.querySelector('#fecha_0').value;

  var banco = document.querySelector('#banco_0').value;

  data['numero'] = numero;
  data['fecha'] = fecha;
  data['banco'] = banco;

  $.ajax({url: "ventas/confirmar_pago/", context: JSON.stringify(data),success: function(result){
      $("#div1").html(result);
    }});
}