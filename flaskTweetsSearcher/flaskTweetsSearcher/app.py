import subprocess
import json, os, math
from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html', result=list())
    # return 'Hello World!'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search', methods=['post', 'get'])
def content_search():
    keyword = request.form.get('search')
    if keyword is None or len(keyword) == 0:
        return render_template('home.html', result=list())

    tmp_h = [["Rank", "Tweets"],
             ["1", "RT @BitcoinMagazine: Twitter went down, #Bitcoin never goes down 🔥"],
             ["2", "RT @_Hugo_Ramos_: I’m in El Zonte! #Bitcoin #ElZonte@stacyherbert @maxkeiser @Excellion https://t.co/93RsEPj5ru"],
             ["3", "@AirdropStario Good project sir 🥳🎉 @tedykia11 @tuyulhandal23 @Tuyulsatu111 #cryptocurrency #Airdrop #BSC #Bitcoin… https://t.co/7VD0OtLpkU"],
             ["4", "What Can Traders Expect With the #Bitcoin(BTC), #Ethereum(ETH), #CARDANO(ADA) Price in the Next 24 Hours? The pos… https://t.co/oQeJkfFlyS"],
             ["5", "RT @Cosmo_Cramer7: @InfinityTokenIO launched yesterday! Look at the #REWARD for their holders. Mining #Bitcoin and returning rewards back t…"],
             ["6", "RT @Dennis_Porter_: BREAKING NEWS: Candidate for Governor of Idaho @JaniceMcGeachin declares she will make “Idaho a safe-haven for #Bitcoin…"],
             ["7", "RT @SafemoonHoly: I'll send $350 in #Bitcoin to one person ⚡🔮 RT and follow me so I can DM! 🔔"],
             ["8", "RT @BitcoinMagazine: 13 years ago today, Satoshi Nakamoto published the first forum post introducing #Bitcoin And the rest is history ✨ ht…"],
             ["9", "RT @FTX_Official: We're giving some #bitcoin away! How much? $1 million worth?! $1.5 million worth?!!?! We don't actually know yet. The l…"],
             ["10", "RT @CryptoHitmann: Excited to announce I am going Full Time #Crypto and why you may want to consider it aswell‼️ #Bitcoin has changed my l…"],
             ]
    if request.form['action'] == 'lucene':
        print('Lucene Search')
        stat, lucene_res = call_jar(keyword)
        return render_template('home.html', result=lucene_res, desc=stat, engine_type='lucene')
    elif request.form['action'] == 'hadoop':
        print('Hadoop Search')
        scores = calculate_score(keyword)
        hadoop_res = get_doc(scores)
        return render_template('home.html', result=hadoop_res, desc='', engine_type='hadoop')


def call_jar(cur_keyword):
    data_dir = "data/tweet_json"
    index_dir = "data/lucene/data_index"
    jar_path = 'data/lucene/jars/lucene_242_project.jar'
    cmd = "java -jar {} {} {} {}".format(jar_path, data_dir, index_dir, cur_keyword)
    clean_dir(index_dir)

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    command_output = process.stdout.read().decode('utf-8')

    res = list()
    stat = None
    if 'index: ' in command_output:
        context_start_idx = command_output.find('index: ')
        command_output = command_output[context_start_idx:]

        lucene_start_idx = command_output.find('1-->')
        stat = command_output[0:lucene_start_idx]

        lucene_res = command_output[lucene_start_idx:]
        lines = lucene_res.split('<END>\n')
        # res = map(lambda a: a.split('-->'), list(filter(None, lines)))
        for line in list(filter(None, lines)):
            res.append(line.split('-->'))
    # res = re.search('index:.*', command_output).group()
    return stat, res


def calculate_score(keyword):
    f_tf = 'data/hadoop/tf/part-r-00000'
    f_idf = 'data/hadoop/idf/part-r-00000'
    ori_path = "data/ori_test.json"
    tf = read_file(f_tf)
    idf = read_file(f_idf)
    ori = read_file(ori_path)

    total_line = len(ori.split('\n')) - 1
    idf_dict = dict()
    try:
        for line in idf.split('\n'):
            item = line.split('\t')
            if item is None or len(item) == 0 or item == ['']:
                continue
            idf_dict[item[0]] = math.log(total_line / (float(item[1]) + 1), 10)
        # idf_dict = map(lambda l: l.split('\t'), idf.split('\n'))
    except IndexError as e:
        print(e)

    tf_idf_dict = dict()
    for line in tf.split('\n'):
        if line is None or len(line) == 0:
            continue
        word, tmp = line.split(':')
        obj_id, tmp = tmp.split('#')
        term_cnt, term_freq = tmp.split('\t')
        if word not in tf_idf_dict:
            tf_idf_dict[word] = dict()
        if word not in idf_dict:
            continue
        tf_idf_dict[word][obj_id] = float(term_freq) * float(idf_dict[word])
    return tf_idf_dict[keyword]


def get_doc(scores):
    res = list()
    ori_path = "data/ori_test.json"
    ori = read_file(ori_path)
    for line in ori.split('\n'):
        if line is None or len(line) == 0:
            continue
        one = json.loads(line)
        obj_id = one['_id']['$oid']
        if obj_id in scores.keys():
            text = one['text']
            retweet = one['retweet_count']
            score = scores[obj_id]
            res.append([score, text, retweet])

    def get_rank(elem):
        return elem[0]
    res.sort(key=get_rank, reverse=True)
    cnt = 1
    hadoop_res = list()
    for line in res:
        if cnt > 10:
            continue
        line = [str(cnt)] + line
        hadoop_res.append(line)
        cnt += 1
    return hadoop_res


def read_file(path):
    content = None
    f = open(path)
    content = f.read()
    f.close()
    return content


def clean_dir(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            clean_dir(c_path)
        else:
            os.remove(c_path)


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 80))
    # app.run(debug=True,host='0.0.0.0',port=port)
    app.run(debug=True)
