import os
jar_path = os.path.join(os.path.abspath('.'), r'data\lucene_242_project.jar')  # jar包路径


def test():
    import jpype
    # jvmPath_32 = r'D:\Program Files\Java\jre_32\bin\client\jvm.dll'  # jre路径
    # jvmPath = r'/Library/Java/JavaVirtualMachines/jdk-16.0.2.jdk/Contents/Home/lib/server/libjvm.dylib'  # jre路径
    jvm_options = [
        # '-Xms{minimum_heap_size}'.format(minimum_heap_size=minimum_heap_size),
        # '-Xmx{maximum_heap_size}'.format(maximum_heap_size=maximum_heap_size),
        '-Djava.class.path={classpath}'.format(classpath=jar_path)
    ]
    jvmPath = jpype.getDefaultJVMPath()
    jpype.startJVM(jvmPath, 'ea', *jvm_options)  # 启动虚拟机
    JClass = jpype.JClass('main.java')
    instance = JClass()
    sum = instance.main('/Users/luyao/Workspace/JavaProjects/Lucene/dataindex',
                        '/Users/luyao/Workspace/JavaProjects/Lucene/data/tweet_json', 'bitcoin')
    print(sum)
    jpype.shutdownJVM()


tmp_dict = {'phy': 50, 'che': 60, 'maths': 70}
tmp_dict = [[1, 2, 3], ["a", "b", "c"]]


# @app.route("/result", methods=['GET', 'POST'])  # 注册路由，并指定HTTP方法为GET、POST
# def result():  # resul函数
#     if request.method == "GET":  # 响应GET请求
#         key_word = request.args.get('word')  # 获取搜索语句
#
#     if len(key_word) != 0:
#         infoso = query("./glxy")  # 创建查询类query的实例
#         re = infoso.search(key_word)  # 进行搜索，返回结果集
#         so_result = []
#         n = 0
#         for item in re["url"]:
#             temp_result = {"url": item, "title": re["title"][n]}  # 将结果集传递给模板
#             so_result.append(temp_result)
#             n = n + 1
#         return render_template('result.html', key_word=key_word, result_sum=re["Hits"], result=so_result)
#     else:
#         key_word = ""
#     return render_template('result.html')




    # return render_template('result.html', result=dict)
    # try:
    # 	#通过model层的News对象，在数据库中检索信息
    #     news_search = News.query.filter(News.title.like("%" + keyword + "%")).all()
    #     print('------------------------------------')
    #     print(news_search)
    #     print('-----------------------------------')
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="搜索内容失败")
    #
    # # 4.将新闻对象列表转成,字典列表
    # search_news_list = []
    # for item in news_search:
    #     search_news_list.append(item.to_dict())
    #
    # # 5.查询所有的分类数据
    # try:
    #     categories = Category.query.all()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="获取分类失败")
    #
    # # 6.将分类的对象列表转成,字典列表
    # search_category_list = []
    # for category in categories:
    #     search_category_list.append(category.to_dict())
    #
    # # 7.拼接用户数据,渲染页面
    # data = {
    #     # 如果user有值返回左边的内容, 否则返回右边的值
    #     "user_info": g.user.to_dict() if g.user else "",
    #     "news_list": search_news_list,
    #     "category_list": search_category_list,
    # }
    # # 渲染页面
    # return render_template("news/search.html", data=data)


