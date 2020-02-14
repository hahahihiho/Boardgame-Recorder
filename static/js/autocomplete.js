// Function: autocompete(inp,arr), autocompleteComma(inp,arr)


// 자동완성(input 위치, 자동완성할 list)
function autocomplete(inp, arr) {
  // 선택한 item 위치 -> input 선택시 -1
  var currentFocus;
  // input event
  inp.addEventListener("input", function(e) {
    // a -> autocomplete-items
    // b -> autocomplete-item
    // i -> index
    // this = e.target
    // val = inputed value
    var a, b, i, val = this.value;

		/*close any already open lists of autocompleted values*/
		closeAllLists();
		if (!val) { return false;}
		currentFocus = -1;
    
    /*create a DIV element that will contain the items (values):*/
		a = document.createElement("DIV");
		a.setAttribute("id", this.id + "autocomplete-list");
		a.setAttribute("class", "autocomplete-items");
		/*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);
    
    // compare val vs arr[]
    for (i = 0; i < arr.length; i++) {
      // check arr[_] contains val
      for(j = 0 ; j < arr[i].length; j++){
        if(arr[i].substr(j,val.length).toUpperCase() == val.toUpperCase()) {
          b = document.createElement("DIV");
          b.innerHTML = arr[i].substr(0,j);
          b.innerHTML += "<strong>" + arr[i].substr(j, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(j+val.length);
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

          // attach click event
          b.addEventListener("click", function(e) {
            /*insert the value for the autocomplete text field:*/
            inp.value = this.getElementsByTagName("input")[0].value;
            // close list
            closeAllLists();
          });
          a.appendChild(b);
          // prevent duplication
          break;
        }
      }
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  
  // add and remove class(autocompete-active)
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

// Comma 단위 autocomplete
function autocompleteComma(inp, arr) {
  // 선택한 item 위치 -> input 선택시 -1
  var currentFocus;
  // input event
  inp.addEventListener("input", function(e) {
    // a -> autocomplete-items
    // b -> autocomplete-item
    // i -> index
    // this = e.target
    // val = inputed value
    var a, b, i, val = this.value;

    // autocomplete 랑 차이 -> 어떻게 모듈화를할까..
    let last_comma = val.lastIndexOf(',');
    let pre_val = val.substr(0,last_comma+1)
    val = val.substr(last_comma+1).trim()
    

		/*close any already open lists of autocompleted values*/
		closeAllLists();
		if (!val) { return false;}
		currentFocus = -1;
    
    /*create a DIV element that will contain the items (values):*/
		a = document.createElement("DIV");
		a.setAttribute("id", this.id + "autocomplete-list");
		a.setAttribute("class", "autocomplete-items");
		/*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);

    // compare val vs arr[]
    for (i = 0; i < arr.length; i++) {
      // check arr[_] contains val
      for(j = 0 ; j < arr[i].length; j++){
        if(arr[i].substr(j,val.length).toUpperCase() == val.toUpperCase()) {
          b = document.createElement("DIV");
          b.innerHTML = arr[i].substr(0,j);
          b.innerHTML += "<strong>" + arr[i].substr(j, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(j+val.length);
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

          // attach click event
          b.addEventListener("click", function(e) {
            /*insert the value for the autocomplete text field:*/
            inp.value =pre_val + this.getElementsByTagName("input")[0].value;
            // close list
            closeAllLists();
          });
          a.appendChild(b);
          // prevent duplication
          break;
        }
      }
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  
  // add and remove class(autocompete-active)
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

