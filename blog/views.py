from django.db.models import Q #本文内容検索の為インポート
from django.shortcuts import get_object_or_404,redirect
from django.views import generic
from .forms import CommentCreateForm
from .models import Post,Category,Comment

class IndexView(generic.ListView):
    model = Post #post_list.htmlが使われる　model名_list.html
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.order_by("-created_at")
        #最新記事から上にリストされるようになる フィールド名を引数にする　-(マイナス)をつけることで降順になる
        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
                )
            #title=keywordだけだと検索とタイトルが完全一致出ないとダメ
            #title__containsだと大文字と小文字を厳密に区別する
        return queryset    


class CategoryView(generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        """
        category = get_object_or_404(Category, pk = self.kwargs['pk'])
        queryset = Post.objects.order_by("-created_at").filter(category = category)
        """
        category_pk = self.kwargs['pk']
        queryset = Post.objects.order_by("-created_at").filter(category__pk = category_pk)        
        return queryset  


class DetailView(generic.DetailView):
    model = Post 

class CommentView(generic.CreateView):
    model = Comment
    #fields = ('name','text') この書き方ならforms.pyはなしで良い
    form_class = CommentCreateForm#この書き方はforms.pyが必要だがフォームのUIをいじれる

    def form_valid(self,form):
        post_pk = self.kwargs['post_pk']
        comment = form.save(commit=False)#コメントはDBに保存されていない　モデルインスタンスの取得
        comment.post = get_object_or_404(Post, pk = post_pk)
        comment.save() #ここでDBに保存
        return redirect('blog:detail',pk = post_pk)
