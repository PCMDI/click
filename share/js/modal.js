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
        var el = document.getElementById(element.dataset.yaxisleft)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.yaxis.increment",function(e){
        console.log("yaxis.increment")
        var el = document.getElementById(element.dataset.yaxisright)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.triangle.decrement",function(e){
        console.log("triangle.decrement")
        var el = document.getElementById(element.dataset.triangleleft)
        if(el){
            element = el
            populateModal()
        }
    })
    $("#modal-content").on("click", ".btn.triangle.increment",function(e){
        console.log("triangle.increment")
        var el = document.getElementById(element.dataset.triangleright)
        if(el){
            element = el
            populateModal()
        }
    })

    $('#tooltip-modal').on('show.bs.modal', function (event) {
        populateModal()
    })
});

function populateModal(){
    var container = $('#modal-content')
    var content = getContent(element)
    container.empty()
    container.append(content)
}

function getContent(el){
    var new_elements = []
    var prev_disabled;
    var next_disabled;

    prev_disabled = el.dataset["xaxisleft"] ? "" : "disabled"
    next_disabled = el.dataset["xaxisright"] ? "" : "disabled"
    new_elements.push(
        $("".concat(
            "<div id=current-xaxis>",
                "<button type='button' class='btn btn-outline-info btn-sm xaxis decrement' style='line-height: 5px'", prev_disabled,"> &lsaquo; </button>",
                "<button type='button' class='btn btn-outline-info btn-sm xaxis increment' style='line-height: 5px'", next_disabled,"> &rsaquo; </button>",
                "<span class='field-label' style='margin-left: 4px;'>", el.dataset["xaxisname"], ": </span>",
                "<span class='field-value'>",
                el.dataset["xaxis"],
                " </span>",
            "</div>"
        ))
    )

    prev_disabled = el.dataset["yaxisleft"] ? "" : "disabled"
    next_disabled = el.dataset["yaxisright"] ? "" : "disabled"
    new_elements.push(
        $("".concat(
            "<div id=current-yaxis>",
                "<button type='button' class='btn btn-outline-info btn-sm yaxis decrement' style='line-height: 5px'", prev_disabled,"> &lsaquo; </button>",
                "<button type='button' class='btn btn-outline-info btn-sm yaxis increment' style='line-height: 5px'", next_disabled,"> &rsaquo; </button>",
                "<span class='field-label' style='margin-left: 4px;'>", el.dataset["yaxisname"], ": </span>",
                "<span class='field-value'>",
                el.dataset["yaxis"],
                " </span>",
            "</div>"
        ))
    )

    if(element.dataset["Triangle"]){
        prev_disabled = el.dataset["triangleleft"] ? "" : "disabled"
        next_disabled = el.dataset["triangleright"] ? "" : "disabled"
        new_elements.push(
            $("".concat(
                "<div id=current-triangle>",
                    "<button type='button' class='btn btn-outline-info btn-sm triangle decrement' style='line-height: 5px'", next_disabled,"> &lsaquo; </button>",
                    "<button type='button' class='btn btn-outline-info btn-sm triangle increment' style='line-height: 5px'", next_disabled,"> &rsaquo; </button>",
                    "<span class='field-label' style='margin-left: 4px;'>", el.dataset["triangelname"], ": </span>",
                    "<span class='field-value'>",
                    el.dataset["Triangle"],
                    " </span>",
                "</div>"
            ))
        )
    }

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

    new_elements.push(
        $("".concat("<img class='full-image' style='margin: 0 auto; width: 100%; max-height: calc(100% - 300px);' src='", el.dataset["image"], "'>"))
    )
    return new_elements
}
