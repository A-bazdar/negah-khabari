/**
 * Created by Morteza on 1/4/2016.
 */
$('head').append("<style>.__border_inspect{border: 3px solid #000000 !important;}</style>");
$(document).on('mousemove', function(e) {
    $(e.target).addClass('__border_inspect');
});
$(document).on('mouseout', function(e) {
    $(e.target).removeClass('__border_inspect');
});
$(document).on('click', function(e) {
    e.preventDefault();
    var path, node = $(e.target);
    while (node.length) {
        var realNode = node[0], name = realNode.localName;
        if (!name) break;
        name = name.toLowerCase();
        var _class = node[0].className;
        var _id = node[0].id;

        var parent = node.parent();
        _class = _class.replace(/ /g, '.').replace(".__border_inspect", "").replace("__border_inspect", "");
        if (_class == "" && _id == "") {
            var sameTagSiblings = parent.children(name);
            if (sameTagSiblings.length > 1) {
                var allSiblings = parent.children();
                var index = allSiblings.index(realNode) + 1;
                if (index > 1) {
                    name += ':nth-child(' + index + ')';
                }
            }
        }else{
            if(_id != ""){
                name += '#' + _id;
            }else{
                name += '.' + _class;
            }
        }
        path = name + (path ? '>' + path : '');
        node = parent;
    }
    alert(path);
});