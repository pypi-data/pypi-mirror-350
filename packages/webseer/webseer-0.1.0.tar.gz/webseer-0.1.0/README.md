<div align='center'>

# ✨Webseer✨

_Webseer —— 专注于“值得获取”的网络情报!_

</div>

**Webseer** 是一个**语义驱动的网络情报者**，根据用户定义的关注点，从互联网上主动搜集并结构化相关信息。  
与传统爬虫不同，**Webseer 以目标为导向地探索网络，理解内容、追踪语义，而不是盲目抓取所有链接。**

## 🚀 核心特性

- 🎯 **聚焦用户兴趣**：你只需提供主题和初始 URL，Webseer 将围绕它构建相关知识库。

- 🧠 **智能内容识别**：智能识别网页中的有意义信息块，跳过冗余噪声。

- 🔗 **语义驱动的链接跟踪**：基于内容理解，而非页面结构进行深度爬取。

- ♻️ **递归式洞察网络构建**：多层级递进抓取构建语义关联的知识网络。

- 🧾 **结构化输出**：输出结构良好的知识数据，便于分析与复用。



## 🧠 与众不同之处？

> 传统爬虫什么都爬。**Webseer** 只获取值得被收集的内容。

它更像是一位研究助理，而不是一个机器人 —— 它执行**上下文搜索**、**信息提炼**和**结构化发现**等高级任务。


## 📦 安装

要安装 Webseer，只需运行以下命令：

```bash
pip install webseer
```

OR

```bash
git clone .....
```

## 🧪 示例用法

```python
import os
from webseer import Seer
from transformers import AutoModel, AutoModelForCausalLM,AutoTokenizer


encode_model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True).to('cuda')

# readertokenizer = AutoTokenizer.from_pretrained("jinaai/ReaderLM-v2")
# readerlm = AutoModelForCausalLM.from_pretrained("jinaai/ReaderLM-v2").to('cuda')

# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
# llm = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct").to('cuda')

# 单关注点
async def single_focus():
    focus = ''
    urls = []  
    await webseer.crawler(focus=focus,urls=urls,llm=None,tokenizer=None)

# 多关注点
async def multi_focus():
    focus_urls = {
                    '关注点1':[],
                    '关注点2':[]
                }
    await webseer.multicrawler(focus_urls=focus_urls,llm=None,tokenizer=None)

if __name__ == "__main__":

    logger_dir = ''
    if not logger_dir:
        current_dir = os.path.dirname(Path(__file__))
        logger_dir = os.path.join(current_dir, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    webseer = Seer(host,port,user,password,logger_dir,encode_model,extract_method='selector',max_request_retries=3,readerlm=None,readertokenizer=None,title_selectors=None, date_selectors=None, author_selectors=None, text_selectors=None)
    
    asyncio.run(single_focus())
```


## 💼 适用场景

- **舆情分析**：舆情分析：自动抓取并结构化分析新闻、社交平台等公开网页内容，追踪特定事件、人物或话题的舆论动态和发展趋势。

- **内容聚合**：适用于新闻聚合、行业资讯采集等业务，支持多源内容统一提取与处理。

- **知识管理**：将零散的网页信息提取为结构化知识，用于构建主题知识库或支撑内部问答系统。

- **企业情报收集**：自动化监测竞品、行业新闻及政策发布等内容，辅助战略分析和决策。

- **深度研究**：自动化收集相关数据快速构建报告所需数据，生成深度报告。


## 📍 开发计划

- [] 增加API数据获取（智谱，Jinaai等）

- [] 增加信息源（公众号，RSS等）

- [] 增加评论数据获取

- [] 增加多平台获取（微博、抖音等）

- [] 增加视频数据获取


## ✨ 命名含义

> Webseer = Web（网络） + Seer（预见者，洞察者）

这个名字表达了项目的使命：通过智能语义探索挖掘真正有价值的信息，而非暴力抓取一切内容。


## 借鉴
本项目受到以下项目的启发：
- wiseflow：https://github.com/TeamWiseFlow/wiseflow/tree/master
- GeneralNewsExtractor：https://github.com/GeneralNewsExtractor/GeneralNewsExtractor

