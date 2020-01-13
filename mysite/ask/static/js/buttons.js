
$("button").click(function(){
    $method = $(this).attr('id');
    $post_id= $(this).attr('name');
    $url = "/like";

      $.ajax({
               type: "POST",
          url: $url,
          data: {
                   'post': $post_id,
                   'method': $method,
                   'csrfmiddlewaretoken': '{{ csrf_token }}'

               },
               dataType: "json",
               success: function(response) {
                      console.log($method,$post_id,$url);
                      console.log(response.message);
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    });