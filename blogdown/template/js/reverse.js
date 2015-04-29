(function (window, document) {
    /*
     * inherit.js is a hacky solution for calculating a font color to
     * coerce element nodes (containing text; nodes existing at the same depth as this script)
    */
    var DEBUG = false;

    //TODO: finish auto picking colors
    var darkOrLight = function(red, green, blue) {
        var brightness;
        brightness = (red * 299) + (green * 587) + (blue * 114);
        brightness = brightness / 255000;

        // values range from 0 to 1
        // anything greater than 0.5 should be bright enough for dark text
        if (brightness >= 0.5) {
          return "dark-text";
        } else {
          return "light-text";
        }
      }



    // adding addKey(s) to underscore.js
    _.mixin({

        findKey: function(obj, search, context) {
            var result,
                isFunction = _.isFunction(search);

                _.any(obj, function (value, key) {
                var match = isFunction ? search.call(context, value, key, obj) : (value === search);
                if (match) {
                    result = key;
                    return true;
                }
            });

          return result;
        },

        findKeys: function(obj, search, context) {
          var result = [],
              isFunction = _.isFunction(search);

          _.each(obj, function (value, key) {
            var match = isFunction ? search.call(context, value, key, obj) : (value === search);
            if (match) {
              result.push(key);
            }
          });

          return result;
        }
    });

    function getStyles (selector){
        if (DEBUG) console.log(selector);
        var re = new RegExp('(^|,)\\s*'+selector.toLowerCase()+'\\s*(,|$)');
        //var styles = {};
        var styles = [];
        $.each ($.makeArray(document.styleSheets), function(){
            if (DEBUG) console.log("document.styleSheet", this.cssRules);

            if (this.cssRules || this.rules){
                if (DEBUG) console.log("document.styleSheet has rules", this);

                $.each (this.cssRules || this.rules, function(){
                    if (DEBUG) console.log("cssRule", this);

                    //if (re.test(this.selectorText) ){
                    if (this.selectorText && this.selectorText.indexOf(selector) != -1){
                      //if(this.style.cssText.indexOf("color") > -1){
                        //styles += this.style.cssText + ';';
                        //styles[this.selectorText] = this.style.cssText;
                        //styles.push([this.selectorText, this.style.cssText]);
                        styles.push(this);
                      //}
                      }
                    });
                }
          });
        return styles;
     }

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

    function getClassNames(node) {
        return _.map($(node).find('*'),
                     function(n){ return n.className; });
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

    // Generate bag-of-words structure
    // (freq. distribution of classes
    var classnames = _.flatten(_.map(sibs,
                                     function(s){
                                        return getClassNames(s);
                                        })),
        classes = _.flatten(_.map(classnames,
                                  function(n) {
                                    return s.words(n);
                                    })),
        classes = _.flatten(_.map(classes,
                                  function(n) {
                                    return s.words(n,/-/);
                                    })),
        wordcounter = {}; // freq. distribution structure

    // count words
    _.each(classes,
           function(n) {
            wordcounter[n] = wordcounter[n] + 1 || 1;
            });

    // most frequent class selector text(s) as
    // split and joined strings (by '-')
    var commonwords = _.findKeys(wordcounter,
                                    _.max(wordcounter)),
        joinedwords = _.reduce(commonwords,
                                  function(memo, val){
                                    return memo + "-" + val;
                                    });

    // get styles containing the above classes
    var styles = getStyles(joinedwords) ||
        _.map(commonwords, function(w){
                return getStyles(w);
            }),
        colorstyles = _.filter(styles, function(s) {
           return s.cssText.indexOf('color') != -1;
        });


}(this, this.document));
