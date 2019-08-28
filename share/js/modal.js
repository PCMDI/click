var element;
$( document ).ready(function() {
    var modal = ''.concat(
        '<div class="modal fade" id="tooltip-modal" tabindex="-1" role="dialog" aria-hidden="true">',
        '<div class="modal-dialog modal-lg" role="document">',
            '<div class="modal-content">',
            '<div class="modal-header">',
                '<h5 class="modal-title" id="tooltipModalLabel"></h5>',
                '<button type="button" class="close" data-dismiss="modal" aria-label="Close">',
                '<span aria-hidden="true">&times;</span>',
                '</button>',
            '</div>',
            '<div id="modal-content" class="modal-body">',
            '</div>',
            '<div class="modal-footer">',
                '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>',
            '</div>',
            '</div>',
        '</div>',
        '</div>'
    )
    $(document.body).append(modal)
    
    // We need to guarantee that the modal will exist. 
    // So we add it with javascript, rather than hoping that the user includes it in their script. 

    $("map").on("click", "area",function(e){
        e.preventDefault()
        element = e.target
        jQuery('#tooltip-modal').modal()
    })
    $("#modal-content").on("click", ".btn.xaxis.decrement",function(e){
        console.log("xaxis.decrement")
        var el = document.getElementById(element.dataset.xaxisleft)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.xaxis.increment",function(e){
        console.log("xaxis.increment")
        var el = document.getElementById(element.dataset.xaxisright)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.yaxis.decrement",function(e){
        console.log("yaxis.decrement")
        var el = document.getElementById(element.dataset.yaxisdown)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.yaxis.increment",function(e){
        console.log("yaxis.increment")
        var el = document.getElementById(element.dataset.yaxisup)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.sector.decrement",function(e){
        console.log("sector.decrement")
        var el = document.getElementById(element.dataset.sectorleft)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.sector.increment",function(e){
        console.log("sector.increment")
        var el = document.getElementById(element.dataset.sectorright)
        if(el){
            element = el
            populateModal()
        }
    })

    $('#tooltip-modal').on('show.bs.modal', function (event) {
        populateModal()
    })
});


function jsonPrettyHighlightToId(jsonobj) {
    
    var json = JSON.stringify(jsonobj, undefined, 2);
    
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    json = json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'color: darkorange;';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'color: red;';
            } else {
                cls = 'color: green;';
            }
        } else if (/true|false/.test(match)) {
            cls = 'color: blue;';
        } else if (/null/.test(match)) {
            cls = 'color: magenta;';
        }
        return '<span style="' + cls + '">' + match + '</span>';
    });
    
   return json;
    
}


function expandJson() {
    var coll = document.getElementsByClassName("collapsible")
    var i;
    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      });
    }
    
}
function populateModal(){
    var container = $('#modal-content')
    var content = getContent(element)
    container.empty()
    container.append(content)
    expandJson()
}

function getContent(el){
    var new_elements = []
    var prev_disabled;
    var next_disabled;

    if(element.dataset["xaxis"]){
        prev_disabled = el.dataset["xaxisleft"] ? "" : "disabled"
        next_disabled = el.dataset["xaxisright"] ? "" : "disabled"
        new_elements.push(
            $("".concat(
                "<div id=current-xaxis>",
                    "<button type='button' class='btn btn-outline-info btn-sm xaxis decrement' style='line-height: 5px'", prev_disabled,"> &#8592; </button>",
                    "<button type='button' class='btn btn-outline-info btn-sm xaxis increment' style='line-height: 5px'", next_disabled,"> &#8594; </button>",
                    "<span class='field-label' style='margin-left: 4px;'>", el.dataset["xaxisname"], ": </span>",
                    "<span class='field-value'>",
                    el.dataset["xaxis"],
                    " </span>",
                "</div>"
            ))
        )
    }

    if(element.dataset["yaxis"]){
        prev_disabled = el.dataset["yaxisdown"] ? "" : "disabled"
        next_disabled = el.dataset["yaxisup"] ? "" : "disabled"
        new_elements.push(
            $("".concat(
                "<div id=current-yaxis>",
                "<button type='button' class='btn btn-outline-info btn-sm yaxis decrement' style='line-height: 5px'", prev_disabled, "> &#8595; </button>",
                "<button type='button' class='btn btn-outline-info btn-sm yaxis increment' style='line-height: 5px'", next_disabled, "> &#8593; </button>",
                "<span class='field-label' style='margin-left: 4px;'>", el.dataset["yaxisname"], ": </span>",
                "<span class='field-value'>",
                el.dataset["yaxis"],
                " </span>",
                "</div>"
            ))
        )
    }

    if(element.dataset["sector"]){
        prev_disabled = el.dataset["sectorleft"] ? "" : "disabled"
        next_disabled = el.dataset["sectorright"] ? "" : "disabled"
        new_elements.push(
            $("".concat(
                "<div id=current-sector>",
                    "<button type='button' class='btn btn-outline-info btn-sm sector increment' style='line-height: 5px'", prev_disabled,"> &#10226; </button>",
                    "<button type='button' class='btn btn-outline-info btn-sm sector decrement' style='line-height: 5px'", next_disabled,"> &#10227; </button>",
                    "<span class='field-label' style='margin-left: 4px;'>", el.dataset["sectorname"], ": </span>",
                    "<span class='field-value'>",
                    el.dataset["sector"],
                    " </span>",
                "</div>"
            ))
        )
    }

    if(element.dataset["value"]){
        new_elements.push(
            $("".concat(
                "<div id=current-value>",
                    "<button type='button' class='btn btn-outline-secondary btn-sm' style='visibility:hidden;' disabled> &lsaquo; </button>",
                    "<button type='button' class='btn btn-outline-secondary btn-sm' style='visibility:hidden;' disabled> &rsaquo; </button>",
                    "<span class='field-label' style='margin-left: 4px;'>Value: </span>",
                    "<span class='field-value'>",
                    el.dataset["value"],
                    " </span>",
                "</div>"
            ))
        )
    }

    if(element.dataset["image"]){
        new_elements.push(
            $("".concat("<img class='full-image' style='margin: 0 auto; width: 100%; max-height: calc(100% - 300px);' src='", el.dataset["image"], "'>"))
        )
    }
    if(element.dataset["json"]){
        var a
        $.ajaxSetup({
            async: false
        });
        var myjson = $.getJSON(el.dataset["json"], a, function(data) {a=data})
        $.ajaxSetup({
            async: true
        });
        var pretty = jsonPrettyHighlightToId(myjson.responseJSON)
        new_elements.push(
            $("".concat("<br><button class='collapsible'>Provenance and Additional Statistics</button>",
            "<div class='content' style='padding: 0 18px; display: none; overflow: hidden; background-color: #f1f1f1; '>",
            "<a href='",el.dataset["json"],"'>JSON FILE</a><br>", pretty, "</div>"))
        )
    }
    return new_elements
}
