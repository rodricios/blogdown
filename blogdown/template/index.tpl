% rebase('base.html')
% setdefault('content_subhead', 'content subhead here')

<!--DEFAULTS FOR post.html-->
<%
setdefault('tagline', 'tagline here')
setdefault('nav_list', ['nav', 'list'])
setdefault('post_title', 'post title here')
setdefault('post_author', 'post author here')
setdefault('post_tags', 'post tags here')
setdefault('post_description', 'post description here')
setdefault('author_avatar', 'author avatar here')
%>

<!-- A wrapper for all the blog posts -->
<div class="posts">
    <h1 class="content-subhead"></h1>

    <div class="post-description">
        <section class="post">
            {{!body}}
        </section>
    </div>
</div>
