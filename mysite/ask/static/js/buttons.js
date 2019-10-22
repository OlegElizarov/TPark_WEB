 function myFunction1() {
        var el=document.getElementsByClassName("btn-group-vertical");
        el=el.getAttribute("id");
          document.getElementById(el).stepUp(1);
      }
      function myFunction2(str) {
          document.getElementById(str).stepDown(1);
      }