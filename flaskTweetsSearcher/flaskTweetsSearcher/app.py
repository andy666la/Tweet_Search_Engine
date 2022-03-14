import os, re
import subprocess
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

jar_path = os.path.join(os.path.abspath('.'), r'data/lucene/jars/lucene_242_project.jar')  # jar包路径


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
        stat, lucene_res = call_jar(keyword)
        return render_template('home.html', result=lucene_res, desc=stat, engine_type='lucene')
    elif request.form['action'] == 'hadoop':
        print('Hadoop Search')
        return render_template('home.html', result=tmp_h, desc=None, engine_type='hadoop')
    else:
        print('Test')
        stat, lucene_res = call_jar(keyword)
        return render_template('home.html', result=lucene_res, desc=stat, engine_type='test')


def call_jar(cur_keyword):
    data_dir = "data/tweet_json"
    index_dir = "data/lucene/dataindex"
    jar_path = 'data/lucene/jars/lucene_242_project.jar'

    process = subprocess.Popen("java -jar {} {} {} {}".format(jar_path, data_dir, index_dir, cur_keyword), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 80))
    # app.run(debug=True,host='0.0.0.0',port=port)
    app.run(debug=True)
