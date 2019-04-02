$(document).ready(function(){

  var $input = $(".typeahead");
  $input.typeahead({
     source: [
      "item1", "item2"
    ],
    autoSelect: false
  });

  $input.change(function() {
    console.log("input name " + this.name);
    var current = $input.typeahead("getActive");
    console.log("current active is " + current)
//    console.log($("input[name=]")[0])
    if (current) {
      // Some item from your model is active!
      if (current == $input.val()) {
        // This means the exact match is found. Use toLowerCase() if you want case insensitive match.
        console.log("currently active matches");

      } else {
        console.log("partial match with " + current);
        // This means it is only a partial match, you can either add a new item
        // or take the active if you don't want new items
      }
    } else {
      // Nothing is active so it is a new value (or maybe empty value)
      console.log("EMPTY");
    }

  });
});
