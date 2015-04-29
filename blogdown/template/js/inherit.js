(function (window, document) {
    /*
     * inherit.js is a hacky solution for calculating a font color to
     * coerce element nodes (containing text; nodes existing at the same depth as this script)
    */

    //http://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
    function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
    }

    function rgbToHex(r,g,b) {
        return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
    }

    function rgbString(r, g, b){
        return "rgb("+r+","+g+","+b+")";
    }

    var getTextNodesIn = function(el) {
        //http://stackoverflow.com/questions/1018855/finding-elements-with-text-using-jquery
        return $(el).find(":not(iframe)").addBack().contents().filter(function()
            {
                 var $this = $(this);
                 return $this.children().length == 0 && $.trim($this.text()).length > 0;
            });
    };

    //var slf = document.currentScript;
    var scripts = document.getElementsByTagName('script'),
        slf = scripts[ scripts.length - 1], // slf is this script
        par =  slf.parentNode,              // destination of style inheritance
        sibs =_.filter(par.children,
                         function (n) {
                            return (n.tagName!="SCRIPT" &&
                                    n.tagName!="STYLE" &&
                                    n!=slf);
                            }),
        grnpar = par.parentNode,            // parent of parent is source of style inheritance
        aunts = _.filter(grnpar.children,
                         function (n) {
                            return (n.tagName!="SCRIPT" &&
                                    n.tagName!="STYLE" &&
                                    n!=par);
                            });

    var auntcolors = _.map(aunts,
                           function(n) {
                            var cstyle = window.getComputedStyle(n),
                                color = cstyle.getPropertyValue('color')
                                rgb = color.match(/\d+/g);
                                return [parseInt(rgb[0]),
                                        parseInt(rgb[1]),
                                        parseInt(rgb[2])];
                                });

    var avg_r = (_.reduce(auntcolors,
                         function (memo, rgb) {
                            return memo + rgb[0];
                            }, 0)) / auntcolors.length,
        avg_r = Math.round(avg_r),
        avg_g = (_.reduce(auntcolors,
                         function (memo, rgb) {
                            return memo + rgb[1];
                            }, 0)) / auntcolors.length,
        avg_g = Math.round(avg_g),
        avg_b = (_.reduce(auntcolors,
                         function (memo, rgb) {
                            return memo + rgb[2];
                            }, 0)) / auntcolors.length,
        avg_b = Math.round(avg_b);

    // get list of text nodes to update their inherited style
    var textnodes = _.map(sibs,
                   function(s){
                    return getTextNodesIn(s.childNodes);
                });

    /*WATCH OUT! TEXTNODES IS AN ARRAY OF JQUERY OBJECTS*/
    _.each(textnodes, function(s){
        _.each(s, function(c){
            if (c.nodeType != 3) {
                c.style.color = rgbString(avg_r, avg_g, avg_b);
            }
        });
    });

    console.log(textnodes);

}(this, this.document));
