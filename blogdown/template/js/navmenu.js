(function ($){

    function guid() {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                    .toString(16)
                    .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
            s4() + '-' + s4() + s4() + s4();
    }

    //http://stackoverflow.com/questions/1359018/in-jquery-how-to-attach-events-to-dynamic-html-elements
    //TOGGLE MENU (http://codepen.io/brenden/pen/Kwbpyj?editors=110)
    //DRAGGABLE
    $('.nav-menu').on('click', 'a.menu-folder', function(e) {
        e.preventDefault();
        var $this = $(this);
        if ($this.parent().next().hasClass('menu-show')) {
            $this.parent().next().removeClass('menu-show');
            $this.parent().next().slideUp(350);
        } else {
            $this.parent().parent().parent().find('li .menu-inner').removeClass('menu-show');
            $this.parent().parent().parent().find('li .menu-inner').slideUp(350);
            $this.parent().next().toggleClass('menu-show');
            $this.parent().next().slideToggle(350);
        }
    });

    //NON-DRAGGABLE
    //$('.nav-menu').on('click', 'a.menu-folder', function(e) {
    //    e.preventDefault();
    //    var $this = $(this);
    //    if ($this.next().hasClass('menu-show')) {
    //        $this.next().removeClass('menu-show');
    //        $this.next().slideUp(350);
    //    } else {
    //        $this.parent().parent().find('li .menu-inner').removeClass('menu-show');
    //        $this.parent().parent().find('li .menu-inner').slideUp(350);
    //        $this.next().toggleClass('menu-show');
    //        $this.next().slideToggle(350);
    //    }
    //});

    function getPathToParent(node) {
        node = $(node);
        var menuRoot = $('#menu-root');
        var pathToParent = "";

        while (node[0] != menuRoot[0]) {
            pathToParent = node.data('name') + "/" + pathToParent;
            node = $(node).parent();
            if (node === null || node.length === 0) { break;}
        }
        return pathToParent;
    }


    //ADD [SUB]FOLDER
    $('.nav-menu').on('click', 'i.menu-folder-add', function(e) {
        e.preventDefault();
        //prompt for new folder name
        var foldername = prompt("Please give this folder a name")

        if (foldername !== null) {
            //ul/li/a/i
            var $this = $(this);

            //create and hide
            var newfolder = $(
                '<li class="ui-state-default" data-name="'+foldername+'">\
                    <span>\
                        <input disabled="true" class="custom-input" type="text" value="'+foldername+'" placeholder=":name here">\
                        <a class="menu-folder" href="#">\
                            <i class="fa fa-pencil"></i>\
                            <i class="menu-folder-rm fa fa-trash-o"></i>\
                        </a>\
                    </span>\
                </li>').hide();

            var foldercontents = $(
                    '<ul class="menu-inner sortable">\
                        <li class="ui-state-default ui-state-disabled">\
                            <a href="#"><i class="menu-file-add fa fa-file-text-o"></i></a>\
                            <a href="#"><i class="menu-folder-add fi-folder-add"></i></a>\
                        </li>\
                    </ul>');

            var newfile = $(
                '<li class="ui-state-default">\
                    <span>\
                        <input class="custom-input" type="text" placeholder=":name here">\
                        <a class="menu-file" href="#">\
                            <i class="menu-file-rm fa fa-trash-o"></i>\
                        </a>\
                    </span>\
                </li>');

            foldercontents.append(newfile);
            newfolder.append(foldercontents);

            //append to greatgrandparent element
            $this.parent().parent().parent().append(newfolder);

            var pathToParent = getPathToParent(newfolder);

            newfolder.slideToggle(350);

            //make "new_dir" request to bottle.py server
            //$.ajax({
            //      type: "POST",
            //      url: "/new/folder/"+foldername,
            //      data: JSON.stringify(payload),
            //      contentType: "application/json; charset=utf-8",
            //      dataType: "json",
            //      success: function(data){
            //      }
            //});
        }
    });

    //ADD FILE
    $('.nav-menu').on('click', 'i.menu-file-add', function(e) {
        //ul/li/a/i
        var $this = $(this);
        //create and hide
        var newfile = $(
            '<li class="ui-state-default">\
                <span>\
                    <input class="custom-input" type="text" placeholder=":name here">\
                    <a class="menu-file" href="#">\
                        <i class="menu-file-rm fa fa-trash-o"></i>\
                    </a>\
                </span>\
            </li>').hide();

        //append to greatgrandparent element
        $this.parent().parent().parent().append(newfile);
        newfile.slideToggle(350);
    });

    //REMOVE [SUB]FOLDER
    $('.nav-menu').on('click', 'i.fa-trash-o', function(e) {
        if (window.confirm("Are you sure?")) {

            $gpa = $(this.parentNode.parentNode.parentNode);
            $gpa.slideToggle(350, function(){
                $(this).remove();
            });
        }
    });

    //REMOVE FILE
    $('.nav-menu').on('click', 'i.menu-file-rm.fa-trash-o', function(e) {
        if (window.confirm("Are you sure?")) {

            $gpa = $(this.parentNode.parentNode);
            $gpa.slideToggle(350, function(){
                $(this).remove();
            });
        }
    });

    //SAVE SITE
    $('#save-site').on('click', function(e) {


        $.ajax({
              type: "POST",
              url: "/save-site/",
              data: JSON.stringify(payload),
              contentType: "application/json; charset=utf-8",
              dataType: "json",
              success: function(data){
              }
        });
    });

    //EDIT NAME OF FOLDER OR FILE
    $('.nav-menu').on('click', 'i.fa.fa-pencil', function(e) {
        $(this.parentNode).siblings().filter(function(){
            return this.nodeName == "INPUT";
            }).prop('disabled', false).focus();
    });



}(jQuery));

(function(_, $){
    $navmenu = $('.nav-menu>ul');

    function ulToJson(node){}

    //upload to GitHub
    $('.nav-list').on('click', 'span.octicon-cloud-upload', function(e){



    });

}(_, jQuery));
