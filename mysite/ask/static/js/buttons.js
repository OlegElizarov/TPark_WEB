
$("button").click(function(){
    console.log($(this).attr('name'));
    console.log($(this).attr('id'));
      $.ajax({
               type: "POST",
          url: "/like",
          data: {
                   'post': $(this).attr('name'),
                   'val': $(this).attr('id'),
                   'csrfmiddlewaretoken': '{{ csrf_token }}'

               },
               dataType: "json",
               success: function(response) {
                      alert(response.message);
                      console.log('its work');
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    });