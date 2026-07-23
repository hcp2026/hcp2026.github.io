const body = document.body;
const header = document.querySelector("[data-header]");
const navToggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");
const navLinks = Array.from(document.querySelectorAll(".site-nav a"));
const navTargets = navLinks
  .map((link) => ({
    href: link.getAttribute("href"),
    section: document.querySelector(link.getAttribute("href")),
  }))
  .filter((target) => target.href && target.section)
  .filter(Boolean);

const SPEAKERS = {
  "yuhong-dai": {
    "id": "yuhong-dai",
    "name": {
      "zh": "戴彧虹",
      "en": "Yuhong Dai"
    },
    "aff": {
      "zh": "中国科学院数学与系统科学研究院",
      "en": "Academy of Mathematics and Systems Science, CAS"
    },
    "photo": "assets/speakers/yuhong-dai.png",
    "title": {
      "zh": "On exact solutions for large-scale facility location",
      "en": "On exact solutions for large-scale facility location"
    },
    "abstract": {
      "zh": "待定",
      "en": "TBA"
    },
    "bio": {
      "zh": "戴彧虹，中国科学院院士，中国科学院数学与系统科学研究院副院长、研究员，现任中国数学会副理事长，中国运筹学会理事长，国际运筹学会联合会副主席。戴彧虹长期从事优化方法的理论及应用研究，在连续优化、整数规划和应用优化等方面作出了系统的创造性工作，方法和成果得到理论和应用界广泛引用和好评。戴彧虹在MATH. PROG.、SIAM J. OPTIM.等期刊发表论文100余篇，著有合著三部。应邀在2022年国际数学家大会(ICM2022)做45分钟邀请报告，并在第24届国际数学规划大会(ISMP2022)作一小时大会报告。获国家自然科学二等奖(2006；完成人：袁亚湘，戴彧虹)、陈省身数学奖、冯康科学计算奖、首届萧树铁应用数学奖和国际运筹学会联合会会士称号(IFORS Fellow)。"
    }
  },
  "naijun-zhan": {
    "id": "naijun-zhan",
    "name": {
      "zh": "詹乃军",
      "en": "Naijun Zhan"
    },
    "aff": {
      "zh": "北京大学计算机学院",
      "en": "School of Computer Science, Peking University"
    },
    "photo": "assets/speakers/naijun-zhan.jpeg",
    "title": {
      "zh": "On termination of polynomial programs with equality conditions",
      "en": "On termination of polynomial programs with equality conditions"
    },
    "abstract": {
      "zh": "We investigate the termination problem of a family of multi-path polynomial programs (MPPs) over an effective field K, in which all assignments to program variables are polynomials, and test conditions of loops and conditional statements are polynomial equalities. We show that the set of non-terminating inputs (NTI) of such a program is algorithmically computable, which in turn yields the decidability of its termination on a given input – and that on a semi-algebraic set of inputs when K is R. To the best of our knowledge, the considered family of MPPs is hitherto the largest fragment of nonlinear programs for which termination is decidable. We present an explicit recursive function, essentially of Ackermannian growth, to compute the maximal length of ascending chains of polynomial ideals under a control function, thereby providing a complete answer to the questions raised by Seidenberg. This maximal length facilitates a precise complexity analysis of our algorithms for computing the NTI and deciding termination of MPPs. We further extend our approach to programs with polynomial guarded commands and show how an incomplete procedure for MPPs with inequality guards can be obtained. Finally, we show that our decidability result gives rise to a complete method for computing all polynomial equality invariants (of a fixed degree) of polynomial programs.",
      "en": "We investigate the termination problem of a family of multi-path polynomial programs (MPPs) over an effective field K, in which all assignments to program variables are polynomials, and test conditions of loops and conditional statements are polynomial equalities. We show that the set of non-terminating inputs (NTI) of such a program is algorithmically computable, which in turn yields the decidability of its termination on a given input – and that on a semi-algebraic set of inputs when K is R. To the best of our knowledge, the considered family of MPPs is hitherto the largest fragment of nonlinear programs for which termination is decidable. We present an explicit recursive function, essentially of Ackermannian growth, to compute the maximal length of ascending chains of polynomial ideals under a control function, thereby providing a complete answer to the questions raised by Seidenberg. This maximal length facilitates a precise complexity analysis of our algorithms for computing the NTI and deciding termination of MPPs. We further extend our approach to programs with polynomial guarded commands and show how an incomplete procedure for MPPs with inequality guards can be obtained. Finally, we show that our decidability result gives rise to a complete method for computing all polynomial equality invariants (of a fixed degree) of polynomial programs."
    },
    "bio": {
      "zh": "詹乃军，男，1971年5月生，北京大学计算机学院博雅特聘教授，国家杰出青年科学基金获得者。之前，为中科院软件所研究员，中科院特聘研究员，中国科学院大学岗位教授，计算机科学国家重点实验室执行主任。分别在南京大学数学系（1989-1993）和南京大学计算机系（1993-1996）获得学士和硕士学位，在中国科学院软件研究所获得博士学位（1997-2000）。研究方向包括：形式化方法，实时、嵌入式、混成系统，程序验证等。任《Journal of Automated Reasoning》、《Formal Aspects of Computing》、《J. of Logical and Algebraic Methods in Programming》、《Research Direction: Cyber-Physical Systems》、《软件学报》、《计算机研究与发展》《电子学报》、《前瞻科技》等期刊编委，国际会议MEMOCODE和SETTA的指导委员会委员，多个国际会议程序委员会共同主席（如形式化方法旗舰会议FM 2021 和验证领域顶级会议TACAS 2027）和著名国际会议程序委员会委员（如CAV、RTSS、HSCC、ICCPS、EMSOFT等）；在著名国际会议和杂志发表论文150多篇，出版专著2部，编著4部，国际国内著名杂志专刊7辑等。现任CCF形式化方法专委主任。",
      "en": "Naijun Zhan is a Boya distinguished professor in the School of Computer Science of Peking University. He got his BSc and MSc both from Nanjing University, and his PhD from Institute of Software Chinese Academy of Sciences (ISCAS). Prior to join Peking University, he worked at the Faculty of Mathematics and Informatics, Mannheim University, Germany as a research fellow, and afterwards worked at ISCAS as an associate professor, a full professor, and a distinguished professor. His research interests cover formal design of real-time, embedded and hybrid systems, program verification. He is in the editorial boards of Journal of Automated Reasoning, Formal Aspects of Computing, Journal of Logical and Algebraic Methods in Programming, Journal of Software, Journal of Electronics, and Journal of Computer Research and Development and so on, a member of the steering committees of SETTA and MEMOCODE, the pc co-chairs of TACAS 2027, ICFEM 2025, FM 2021 and SETTA 2016, the general co-chairs of SETTA 2025, MEMOCODE 2019, MEMOCODE2018 and ICESS 2019, and serves more than 100 international conferences program committees e.g., CAV, RTSS, HSCC, FM, TACAS, EMSOFT, etc. He published more than 150 papers in international leading journals and conferences and 2 books, and edited 5 conference proceedings and 7 journal special issues. See lcs.ios.ac.cn/~znj for more details."
    }
  },
  "pinyan-lu": {
    "id": "pinyan-lu",
    "kind": "panel",
    "name": {
      "zh": "陆品燕",
      "en": "Pinyan Lu"
    },
    "aff": {
      "zh": "上海财经大学",
      "en": "Shanghai University of Finance and Economics"
    },
    "photo": "assets/speakers/pinyan-lu.jpg",
    "title": {
      "zh": "AI时代的算法研究",
      "en": "Algorithm Research in the AI Era"
    },
    "abstract": {
      "zh": "嘉宾待定",
      "en": "Panelists TBA"
    },
    "bio": {
      "zh": "陆品燕，上海财经大学“长江学者”特聘教授，计算机与人工智能学院创院院长，华为泰勒实验室首席科学家。他的主要研究方向是理论计算机，并注重与其它学科的交叉，近年来也关注求解器算法与大模型机理的研究。曾荣获ACM杰出科学家奖、第八届世界华人数学家大会ICCM数学奖（原晨兴数学奖）银奖、中国计算机学会青年科学家（2014）等荣誉。",
      "en": "Pinyan Lu is a Changjiang Distinguished Professor at Shanghai University of Finance and Economics, founding dean of the School of Computing and Artificial Intelligence, and chief scientist at Huawei Taylor Lab. His main research area is theoretical computer science, with an emphasis on connections with other disciplines. In recent years, he has also worked on solver algorithms and mechanisms of large language models. He has received honors including ACM Distinguished Scientist, the silver medal of the ICCM Mathematics Award at the 8th International Congress of Chinese Mathematicians, and the CCF Young Scientist Award (2014)."
    }
  },
  "xiaoming-sun": {
    "id": "xiaoming-sun",
    "name": {
      "zh": "孙晓明",
      "en": "Xiaoming Sun"
    },
    "aff": {
      "zh": "中国科学院计算技术研究所",
      "en": "Institute of Computing Technology, CAS"
    },
    "photo": "assets/speakers/xiaoming-sun.png",
    "title": {
      "zh": "量子线路优化",
      "en": "Quantum Circuit Optimization"
    },
    "abstract": {
      "zh": "量子计算依托量子叠加、纠缠等独特量子力学效应构建新的计算范式，Shor算法、Grover算法等显示其在特定计算任务上具备超越经典计算的加速潜力。现阶段量子硬件普遍存在量子比特规模有限、相干时间短、门噪声显著等瓶颈，制约各类量子算法在含噪声中规模量子设备上的稳定、高效执行。量子线路综合与优化作为量子编译的重要环节，是缓解硬件噪声约束、提升量子程序运行保真度的关键技术。本报告将梳理线路优化领域的一些核心问题，并汇报课题组在线路化简、硬件适配映射、深度压缩等方向的一些进展，以及衍生出的优化问题。",
      "en": "Quantum computing builds a new computing paradigm on quantum superposition, entanglement, and other distinctive quantum-mechanical effects. Algorithms such as Shor's algorithm and Grover's algorithm demonstrate its potential to outperform classical computing on specific tasks. Current quantum hardware still faces bottlenecks such as limited qubit scale, short coherence time, and significant gate noise, which constrain the stable and efficient execution of quantum algorithms on noisy intermediate-scale quantum devices. Quantum circuit synthesis and optimization, as key components of quantum compilation, are important techniques for mitigating hardware noise constraints and improving the fidelity of quantum program execution. This talk will review several core problems in circuit optimization and present recent progress from our group on circuit simplification, hardware-aware mapping, depth compression, and related optimization problems."
    },
    "bio": {
      "zh": "孙晓明，中国科学院计算技术研究所研究员，量子计算与算法理论实验室主任，国家杰出青年科学基金获得者，中国计算机学会会士。主要研究领域为算法与计算复杂性、量子计算等，曾获王选杰出青年学者奖等。目前担任中国计算机学会量子计算专委会主任，《中国科学:信息科学》《TPAMI》等学术期刊编委。"
    }
  },
  "qilong-feng": {
    "id": "qilong-feng",
    "name": {
      "zh": "冯启龙",
      "en": "Qilong Feng"
    },
    "aff": {
      "zh": "中南大学计算机学院",
      "en": "School of Computer Science and Engineering, Central South University"
    },
    "photo": "assets/speakers/qilong-feng.jpeg",
    "title": {
      "zh": "面向大规模数据的机器学习算法优化",
      "en": "Optimization of Machine Learning Algorithms for Large-Scale Data"
    },
    "abstract": {
      "zh": "随着数据规模的快速增长，传统机器学习算法在计算开销、动态更新和数据约束等方面面临巨大挑战。本报告主要介绍大规模数据场景下机器学习算法优化方法，重点讨论聚类与回归问题的高效算法设计与分析。针对聚类问题，介绍近线性时间算法、增量学习算法，面向动态更新的算法，并讨论如何去除诸多算法依赖的离散度因子。面向数据约束挑战，介绍带公平性约束的模型与算法，以及线聚类等结构化聚类问题的优化思路。在数据维度处理方面，从子集选择角度出发，介绍高效数据降维算法的设计。针对回归问题，从coreset构造和局部搜索等角度出发，介绍如何进行稀疏数据表示和高效算法设计。"
    },
    "bio": {
      "zh": "冯启龙，中南大学计算机学院教授，博士生导师，计算机学院副院长。主要从事计算机算法优化，机器学习基础理论与算法优化等方面的研究。在SODA、NeurIPS、ICML、ICLR、Information and Computation等会议和期刊上发表论文60多篇，出版1本专著，获得省部级奖励2项。主持国家自然科学基金重点项目等项目10余项。担任中国计算机学会理论计算机科学专业委员会常务委员、中国计算机学会人工智能基础委员会通信委员、期刊 Frontiers in Computer Science 青年编委、第 16 届算法与模型应用国际会议程序委员会主席。"
    }
  },
  "yixin-cao": {
    "id": "yixin-cao",
    "name": {
      "zh": "操宜新",
      "en": "Yixin Cao"
    },
    "aff": {
      "zh": "香港理工大学计算学系",
      "en": "Department of Computing, The Hong Kong Polytechnic University"
    },
    "photo": "assets/speakers/yixin-cao.jpeg",
    "title": {
      "zh": "Half-integral Solutions of Linear Systems",
      "en": "Half-integral Solutions of Linear Systems"
    },
    "abstract": {
      "zh": "Most combinatorial optimization problems are NP-hard, which means their integer programming formulations typically lack the total dual integrality property. In the 1970s, Balinski observed that all extreme points of the fractional independent set polytope are half-integral. In this work, we explore further developments in this area. Additionally, we provide a brief discussion on employing graph-theoretical approaches to solve integer programs.",
      "en": "Most combinatorial optimization problems are NP-hard, which means their integer programming formulations typically lack the total dual integrality property. In the 1970s, Balinski observed that all extreme points of the fractional independent set polytope are half-integral. In this work, we explore further developments in this area. Additionally, we provide a brief discussion on employing graph-theoretical approaches to solve integer programs."
    },
    "bio": {
      "zh": "操宜新博士是香港理工大学计算学系的副教授，2012年博士毕业于德州农机大学。在2014年回国之前，他在匈牙利科学院做了两年的研究员。他的研究兴趣包括算法图论，细粒度复杂性和算法设计，组合优化。他的研究得到了香港研究资助委员会（RGC）和国家自然科学基金（NSFC）的支持。目前主要学术兼职包括中国计算机学会理论计算机科学专业委员会常务委员和中国运筹学会数学规划分会理事和图论组合分会理事。"
    }
  },
  "zhendong-lei": {
    "id": "zhendong-lei",
    "name": {
      "zh": "雷震东",
      "en": "Zhendong Lei"
    },
    "aff": {
      "zh": "华为泰勒实验室",
      "en": "Huawei Taylor Lab"
    },
    "photo": "assets/speakers/zhendong-lei.jpg",
    "title": {
      "zh": "从工业应用看模型表达能力与算法设计",
      "en": "从工业应用看模型表达能力与算法设计"
    },
    "abstract": {
      "zh": "随着各领域业务的发展，实际工业问题的规模呈指数级增长，其内在约束与耦合关系日益复杂。这往往导致直接构建的单一数学模型（如混合整数线性规划MILP）面临变量与约束规模爆炸的难题，致使求解难度陡增，甚至无法求解。而当前主流求解器技术多针对特定范式（如SAT、MIP等）独立设计，难以应对此类复杂场景。本报告将从工业应用视角出发，剖析实际场景中蕴含的复杂约束特征，深入探讨模型表达能力与算法设计在实际落地中的权衡关系及效能表现。最后，本报告将介绍泰勒实验室在该方向上的探索与最新研究进展。",
      "en": "随着各领域业务的发展，实际工业问题的规模呈指数级增长，其内在约束与耦合关系日益复杂。这往往导致直接构建的单一数学模型（如混合整数线性规划MILP）面临变量与约束规模爆炸的难题，致使求解难度陡增，甚至无法求解。而当前主流求解器技术多针对特定范式（如SAT、MIP等）独立设计，难以应对此类复杂场景。本报告将从工业应用视角出发，剖析实际场景中蕴含的复杂约束特征，深入探讨模型表达能力与算法设计在实际落地中的权衡关系及效能表现。最后，本报告将介绍泰勒实验室在该方向上的探索与最新研究进展。"
    },
    "bio": {
      "zh": "雷震东，中科院博士，现任华为泰勒实验室，智能决策团队负责人。主要从事运筹优化、约束求解以及机制设计等相关研究工作，有10年求解器研发经验，在国际相关比赛中获得多个冠军。曾获得中科院院长特别奖、华为金牌个人等荣誉。"
    }
  },
  "mingxuan-yuan": {
    "id": "mingxuan-yuan",
    "name": {
      "zh": "袁明轩",
      "en": "Mingxuan Yuan"
    },
    "aff": {
      "zh": "华为诺亚方舟实验室 / 香港诺亚方舟实验室",
      "en": "Huawei Noah's Ark Lab / Hong Kong Noah's Ark Lab"
    },
    "photo": "assets/speakers/mingxuan-yuan.jpg",
    "title": {
      "zh": "基于大模型的自动算法设计",
      "en": "LLM-based Automatic Algorithm Design"
    },
    "abstract": {
      "zh": "过去两年间，基于大模型的自动算法设计方法取得了显著进展，缓解了工业优化问题长期存在的高定制化成本挑战，并有望在优化效率和有效性方面实现阶跃式提升。本次报告将重点介绍基于大模型的自动算法领域的一些探索与进展，包括算法设计空间理解、启发式算法的自动进化框架、基于多模态的算法设计、多分布下的协同进化自动算法设计等，并展示我们最新的LLM4AD Next工具。",
      "en": "Over the past two years, LLM-based automatic algorithm design has made significant progress. It helps reduce the long-standing high customization cost of industrial optimization problems and has the potential to bring step-change improvements in optimization efficiency and effectiveness. This talk will introduce explorations and progress in automatic algorithm design based on large language models, including understanding algorithm design spaces, automatic evolution frameworks for heuristic algorithms, multimodal algorithm design, and co-evolutionary automatic algorithm design across multiple distributions. It will also present our latest LLM4AD Next tool."
    },
    "bio": {
      "zh": "袁明轩，当前担任华为诺亚方舟实验室高级研究员和香港诺亚方舟实验室主任。他博士毕业于香港科技大学，研究兴趣包括学习优化、AI求解器、AI4EDA和大模型应用等。他曾担任华为AI应用创新实验室主任，并主导负责企业智能（供应链优化与企业服务等）、AI4EDA、AI求解器和行业智能项目，带领团队完成了行业大模型应用、供应链（排产引擎、物流数字化装箱装柜、仓库仿真与调度等）、自研求解器替代任务、求解器AI特性、存储智能调度、港口水平调度、EDA自研工具系列算法（比如DSE、逻辑综合、ATPG、LEC、2D/3D布局等等）和电信大数据时空数据分析引擎、用户离网预测等算法与模型研发上线与产品化。同时担任TKDE、KDD、NeurIPS等A类期刊与会议审稿人和TETCI副主编等学术服务职务，完成授权专利50+。",
      "en": "Mingxuan Yuan is currently a Senior Researcher at Huawei Noah's Ark Lab and Director of Hong Kong Noah's Ark Lab. He received his Ph.D. from The Hong Kong University of Science and Technology. His research interests include learning to optimize, AI solvers, AI4EDA, and large language model applications. He previously served as Director of Huawei's AI Application Innovation Lab, where he led projects in enterprise intelligence, including supply-chain optimization and enterprise services, AI4EDA, AI solvers, and industrial intelligence. He has led teams to deliver and productize industrial LLM applications, supply-chain systems such as scheduling engines, logistics packing and container loading, warehouse simulation and dispatching, self-developed solver replacement, AI features for solvers, storage intelligent scheduling, port horizontal transport scheduling, EDA algorithms for self-developed tools including DSE, logic synthesis, ATPG, LEC, 2D/3D placement, telecom big-data spatiotemporal analytics engines, and user churn prediction. He also serves as a reviewer for leading journals and conferences such as TKDE, KDD, and NeurIPS, and as an Associate Editor of TETCI. He has more than 50 granted patents."
    }
  },
  "min-li": {
    "id": "min-li",
    "name": {
      "zh": "李旻",
      "en": "Min Li"
    },
    "aff": {
      "zh": "东南大学集成电路学院",
      "en": "School of Integrated Circuits, Southeast University"
    },
    "photo": "assets/speakers/min-li.png",
    "title": {
      "zh": "面向硬件形式化难例求解的智能体路线",
      "en": "An Agentic Route to Solving Hard Instances in Hardware Formal Verification"
    },
    "abstract": {
      "zh": "硬件形式化验证在复杂芯片设计中承担着发现深层缺陷、保证功能正确性的关键作用，但在实际应用中仍面临状态空间巨大、性质数量庞大、跨抽象层语义差异明显、人工调试成本高等难题。特别是在数据通路电路、多属性验证、等价检查与网表级分析场景中，传统求解流程往往依赖专家经验进行建模、分解、调参和反例分析，难以形成高度自动化、可扩展的验证闭环。本报告围绕“面向硬件形式化难例求解的智能体路线”展开，探讨如何将形式化验证工具、EDA 算法、大模型与电路表征学习结合起来，构建面向难例求解的智能验证系统。报告将结合数据通路等价验证、形式化 bug hunting、RTL 代码演化以及门级网表智能体等研究探索，介绍智能体如何参与电路语义理解、任务分解、求解策略选择、反例分析与代码修复。"
    },
    "bio": {
      "zh": "李旻，现东南大学集成电路学院研究员，2018年获得上海交通大学电子科学与技术专业本科学位，2023年获得香港中文大学（QS排36）计算机科学与工程系博士学位，并于华为诺亚方舟实验室担任主任工程师，负责参与国产自研硬件形式化验证工具，服务于华为多款高性能处理器验证。主要研究领域为人工智能辅助电子设计自动化（EDA）、面向计算芯片的高效形式化验证、人工智能驱动的新一代硬件形式化验证工具等。近五年发表EDA与AI领域顶会，电路表征学习系列研究获得了DAC'22最佳论文提名和来自海思和港府多项研究资助。"
    }
  },
  "hu-qin": {
    "id": "hu-qin",
    "name": {
      "zh": "秦虎",
      "en": "Hu Qin"
    },
    "aff": {
      "zh": "华中科技大学管理学院",
      "en": "School of Management, Huazhong University of Science and Technology"
    },
    "photo": "assets/speakers/hu-qin.jpeg",
    "title": {
      "zh": "车辆路径优化算法：现状、挑战和实践",
      "en": "Vehicle Routing Optimization Algorithms: Status, Challenges, and Practice"
    },
    "abstract": {
      "zh": "本次报告深度聚焦车辆路径优化（VRP）领域，系统解析精确算法与启发式算法的核心分类、底层原理及各自优劣。针对传统方案定制成本高、通用性差的行业痛点，报告创新性地提出“算法框架+独立约束”的灵活求解策略，有效兼顾了运算效率与场景适配性。此外，结合制药企业多模式运输等真实案例，生动展现了该方案在多仓库、多车型、多时间窗等复杂业务场景下的落地成效，切实助力企业降本增效，兼具学术前沿深度与产业实践价值。最后，报告将以可拆分车辆路径优化问题（SDVRP）为例，深入剖析并系统分享启发式算法的核心设计技巧与实战经验。"
    },
    "bio": {
      "zh": "秦虎，华中科技大学管理学院教授、博士生导师，主要研究方向为运筹优化、智能优化算法、网络规划、运输调度与生产排程。主持完成国家自然科学基金项目3项，现承担重点项目和面上项目各1项，在SCI/SSCI期刊发表论文70余篇。自2016年起任管理科学与工程学会管理系统工程分会秘书长。曾获“楚天学者”称号，并入选武汉光谷3551人才计划与江苏省“双创计划”。2018年获京东全球运筹优化挑战赛总冠军，主持多项企业合作项目，服务企业包括华为、顺丰、美的等。2017年创办公众号“数据魔术师”，拥有7万余关注者，致力于运筹优化技术的推广与应用。"
    }
  },
  "yixiao-huang": {
    "id": "yixiao-huang",
    "name": {
      "zh": "黄一潇",
      "en": "Yixiao Huang"
    },
    "aff": {
      "zh": "顺丰科技",
      "en": "SF Technology"
    },
    "photo": "assets/speakers/yixiao-huang.jpeg",
    "title": {
      "zh": "顺丰智能物流网络规划技术分享",
      "en": "SF Express Intelligent Logistics Network Planning Technology Sharing"
    },
    "abstract": {
      "zh": "中国快递市场规模庞大，2025年全年快递业务量接近2000亿件。背后的快递运营网络结构复杂，需要综合权衡服务水平、运营成本等诸多因素。报告阐述如何进行智能物流网络优化的方法论和企业实践。内部团队深入理解实际复杂业务，从中剥离核心数学优化问题，综合分析问题性质和前沿技术方法。利用运筹优化模型显著优化物流网络，支持物流网络重要战略决策，提升决策效率和质量，显著减少碳排放。"
    },
    "bio": {
      "zh": "顺丰科技运筹优化算法高级工程师。参与顺丰网络规划，运营模式创新等算法应用。分别于2012年和2018年获得清华大学工业工程系管理科学与工程学士学位和博士学位。在交通运输优化顶级期刊Transportation Science和Transportation Research Part B等发表多篇论文。曾获2020年INFORMS TSL的子研究领域杰出论文奖，主导顺丰网络规划智能解决方案项目获得2025年INFORMS弗兰兹·厄德曼全球决赛奖。"
    }
  },
  "emanuele-bellini": {
    "id": "emanuele-bellini",
    "name": {
      "zh": "Emanuele Bellini",
      "en": "Emanuele Bellini"
    },
    "aff": {
      "zh": "Technology Innovation Institute (TII), UAE",
      "en": "Technology Innovation Institute (TII), UAE"
    },
    "photo": "assets/speakers/emanuele-bellini.jpeg",
    "title": {
      "zh": "Generating and Solving Hard Symmetric Cryptanalysis Problems with CLAASP",
      "en": "Generating and Solving Hard Symmetric Cryptanalysis Problems with CLAASP"
    },
    "abstract": {
      "zh": "In 2023, we published a large-scale comparison of SAT, SMT, MILP, and CP techniques for differential cryptanalysis across more than 20 symmetric primitives and 16 solvers. The study highlighted that solver performance is highly problem-dependent, with different paradigms excelling on different cipher families and tasks.\n\nBuilding on these results, this talk explores how to create public, reproducible benchmark challenges for symmetric cryptanalysis that are valuable to both solver developers and cryptanalysis researchers. We discuss the difficulties of defining fair and meaningful challenges across diverse attack models, cipher designs, solver paradigms, and evaluation criteria.\n\nWe then present how CLAASP can systematically support such an effort through automated generation of cryptanalytic models, scalable benchmark instances, and baseline evaluations across multiple solvers. The long-term objective is to foster a community-driven collection of solver-oriented symmetric cryptanalysis challenges and benchmarks.",
      "en": "In 2023, we published a large-scale comparison of SAT, SMT, MILP, and CP techniques for differential cryptanalysis across more than 20 symmetric primitives and 16 solvers. The study highlighted that solver performance is highly problem-dependent, with different paradigms excelling on different cipher families and tasks.\n\nBuilding on these results, this talk explores how to create public, reproducible benchmark challenges for symmetric cryptanalysis that are valuable to both solver developers and cryptanalysis researchers. We discuss the difficulties of defining fair and meaningful challenges across diverse attack models, cipher designs, solver paradigms, and evaluation criteria.\n\nWe then present how CLAASP can systematically support such an effort through automated generation of cryptanalytic models, scalable benchmark instances, and baseline evaluations across multiple solvers. The long-term objective is to foster a community-driven collection of solver-oriented symmetric cryptanalysis challenges and benchmarks."
    },
    "bio": {
      "zh": "Emanuele Bellini is Technical Director of Cryptography at the Technology Innovation Institute (TII), UAE. His expertise spans symmetric cryptography, elliptic-curve cryptography, coding theory, and cryptanalysis. He leads several research initiatives, including CLAASP, an automated symmetric cryptanalysis framework, and CryptographicEstimators, a project aggregating security estimates for post-quantum cryptography. He also oversees the development of UAE sovereign cryptographic technologies. Previously, he worked as a cryptographer at DarkMatter (UAE) and Telsy (Italy). He holds a Ph.D. in Coding Theory and Cryptography from the University of Trento and degrees in Mathematics from the University of Turin.",
      "en": "Emanuele Bellini is Technical Director of Cryptography at the Technology Innovation Institute (TII), UAE. His expertise spans symmetric cryptography, elliptic-curve cryptography, coding theory, and cryptanalysis. He leads several research initiatives, including CLAASP, an automated symmetric cryptanalysis framework, and CryptographicEstimators, a project aggregating security estimates for post-quantum cryptography. He also oversees the development of UAE sovereign cryptographic technologies. Previously, he worked as a cryptographer at DarkMatter (UAE) and Telsy (Italy). He holds a Ph.D. in Coding Theory and Cryptography from the University of Trento and degrees in Mathematics from the University of Turin."
    }
  },
  "chunning-zhou": {
    "id": "chunning-zhou",
    "name": {
      "zh": "周春宁",
      "en": "Chunning Zhou"
    },
    "aff": {
      "zh": "南洋理工大学",
      "en": "Nanyang Technological University"
    },
    "photo": "assets/speakers/chunning-zhou.jpg",
    "title": {
      "zh": "Open Cryptanalysis Platform（OCP）：面向对称密码的自动化密码分析平台",
      "en": "Open Cryptanalysis Platform (OCP): An Automated Cryptanalysis Platform for Symmetric Cryptography"
    },
    "abstract": {
      "zh": "随着对称密码算法应用广泛、结构设计日益多样化，自动化密码分析工具在效率、通用性和可扩展性方面面临更高要求。本报告介绍面向对称密码的自动化分析平台 OCP（Open Cryptanalysis Platform）的设计与应用。OCP将分组密码、置换和流密码统一表示为由变量与算子组成的轮/层结构，并在此基础上支持 Python、C 和 Verilog 可执行代码生成、结构可视化、面向密码分析的 MILP/SAT 模型构造以及外部求解器辅助搜索。面向 SPN、ARX 等典型结构，可自动搜索最小活跃 S 盒数量、最优及多条差分、线性和相关密钥差分特征，并通过聚集高概率差分特征或高绝对相关性线性特征来估计差分概率与线性壳相关性。针对 S 盒、异或等基础算子，提供多种 MILP/SAT 建模方法，并集成 Matsui 剪枝约束与基于目标界动态调整的 SAT 优化搜索策略，以提升长轮数搜索效率。目前，OCP已覆盖 AES、PRESENT、GIFT、SKINNY、SPECK 等典型对称密码原语，其模块化和可扩展设计支持新密码算法、新算子、新建模方法与新密码分析任务的快速集成，为对称密码安全评估提供统一平台。"
    },
    "bio": {
      "zh": "周春宁，博士，于中国科学院信息工程研究所获得博士学位，目前在新加坡南洋理工大学 Thomas Peyrin 教授课题组从事博士后研究工作，主要研究方向为对称密码原语的密码分析，包括分组密码、哈希函数的自动化安全性分析。"
    }
  },
  "xindi-zhang": {
    "id": "xindi-zhang",
    "name": {
      "zh": "张昕荻",
      "en": "Xindi Zhang"
    },
    "aff": {
      "zh": "中国科学院软件研究所",
      "en": "Institute of Software, CAS"
    },
    "photo": "assets/speakers/xindi-zhang.png",
    "title": {
      "zh": "SAT求解及其在密码分析中的应用",
      "en": "SAT Solving and Its Applications in Cryptanalysis"
    },
    "abstract": {
      "zh": "SAT是密码分析的重要基础工具，本报告将重点围绕其串、并行求解及LLM加速技术，介绍其在密码分析中的应用。串行求解方面，针对大规模约束冗余的方程组求解问题，本报告将介绍一种动态添加约束的增量求解方法，助力斩获“强网杯”冠军。并行求解方面，将介绍基于多样性与关键变量采样的分治并行求解技术。PRS求解器多次在国际竞赛中夺冠，在密码样例上实现千核规模持续加速，并应用于哈希碰撞分析。最后，介绍大模型辅助的并行SAT求解方法，并在ASCON线性分析中成功突破4轮最优活跃S盒边界。"
    },
    "bio": {
      "zh": "张昕荻，中国科学院软件研究所，助理研究员，长期从事SAT求解及形式化应用的研究，于CAV、SAT、DAC、FM等会议及期刊发表学术论文20余篇。其研究工作获评国际SAT协会“最佳博士学位论文奖”（每年全球一名，亚洲首个）、国际SAT会议“最佳论文奖”（亚洲首个）、中科院优秀博士学位论文等。其研制的求解器曾多次于国际SAT、SMT、FLoC等比赛夺冠，相关技术落地于国内多家头部企业，并应用于密码分析领域，获“强网杯”密码数学专项赛全国冠军。他曾获中科院院长特别奖等荣誉，并获中国教育发展基金会“集成电路人才培养”资助。主持或参与国自然青年基金、网安重大专项、重点研发、国自然重点等项目。"
    }
  },
  "shengxin-liu": {
    "id": "shengxin-liu",
    "name": {
      "zh": "刘圣鑫",
      "en": "Shengxin Liu"
    },
    "aff": {
      "zh": "哈尔滨工业大学（深圳）计算机科学与技术学院",
      "en": "School of Computer Science and Technology, Harbin Institute of Technology (Shenzhen)"
    },
    "photo": "assets/speakers/shengxin-liu.jpg",
    "title": {
      "zh": "Branch-and-Bound Algorithms for Maximum Cohesive Subgraph Search",
      "en": "Branch-and-Bound Algorithms for Maximum Cohesive Subgraph Search"
    },
    "abstract": {
      "zh": "Finding maximum cohesive subgraphs is a fundamental problem in graph mining, with applications in community detection, social network analysis, and related areas. This talk presents our recent work on efficient branch-and-bound algorithms for maximum cohesive subgraph search. The talk covers five representative models—$k$-plex, defective clique, $s$-bundle, degree-based quasi-clique, and edge-based quasi-clique—each providing a different relaxation of the maximum clique model. I will discuss the main algorithmic techniques, including effective branching strategies, reduction rules, and upper bounds, underlying our results published in SIGMOD’25, PVLDB’25, KDD’25, PVLDB’26, and WWW’26. I will conclude with several directions for future research.",
      "en": "Finding maximum cohesive subgraphs is a fundamental problem in graph mining, with applications in community detection, social network analysis, and related areas. This talk presents our recent work on efficient branch-and-bound algorithms for maximum cohesive subgraph search. The talk covers five representative models—$k$-plex, defective clique, $s$-bundle, degree-based quasi-clique, and edge-based quasi-clique—each providing a different relaxation of the maximum clique model. I will discuss the main algorithmic techniques, including effective branching strategies, reduction rules, and upper bounds, underlying our results published in SIGMOD’25, PVLDB’25, KDD’25, PVLDB’26, and WWW’26. I will conclude with several directions for future research."
    },
    "bio": {
      "zh": "刘圣鑫，现任哈尔滨工业大学（深圳）计算机科学与技术学院副教授。博士毕业于香港城市大学，随后在新加坡南洋理工大学从事博士后研究工作。主要研究方向包括图数据管理与算法博弈论，近年来重点开展稠密子图挖掘与资源公平分配等方面的研究。其相关研究成果曾获AAAI最佳学生论文奖和FAW最佳论文奖。",
      "en": "Shengxin Liu is an Associate Professor in the School of Computer Science and Technology at Harbin Institute of Technology (Shenzhen). He received his Ph.D. from City University of Hong Kong and then conducted postdoctoral research at Nanyang Technological University, Singapore. His research interests include graph data management and algorithmic game theory. In recent years, his work has focused on dense subgraph mining and fair resource allocation. His related research has received the AAAI Best Student Paper Award and the FAW Best Paper Award."
    }
  },
  "zhaoguo-wang": {
    "id": "zhaoguo-wang",
    "name": {
      "zh": "王肇国",
      "en": "Zhaoguo Wang"
    },
    "aff": {
      "zh": "上海交通大学",
      "en": "Shanghai Jiao Tong University"
    },
    "photo": "assets/speakers/zhaoguo-wang.jpeg",
    "title": {
      "zh": "FM-Agent：面向大型系统软件的霍尔范式自动化推理智能体及领域实战",
      "en": "FM-Agent: Hoare-Style Automated Reasoning Agents for Large-Scale System Software and Real-World Practice"
    },
    "abstract": {
      "zh": "如今的Coding Agent生成十万行以上的系统级代码，甚至构建一个完整的编译器，都已不再稀奇。但一个严峻的挑战随之而来：如何保障这些大规模代码的正确性？为此，我们推出了形式化方法智能体FM-Agent，通过将霍尔逻辑与LLM结合，首次实现了面向大规模软件的全自动正确性推理，在 Anthropic、NVIDIA 等用顶尖编程智能体生成的多个大规模系统（单个系统规模高达 14.3 万行）中，FM-Agent 报告了 522 个潜在 bug。值得关注的是，这些 bug 经过单元测试、差分测试、多智能体交叉审查等手段都未能发现。本次报告将向大家分享FM-Agent的最新进展，以及面向编译器、数据库等系统的实战经验。",
      "en": "Coding agents can now generate more than 100,000 lines of system-level code and even build complete compilers. This raises a serious challenge: how can we ensure the correctness of such large-scale code? We address this challenge with FM-Agent, a formal-methods agent that combines Hoare logic with LLMs. It is the first system to achieve fully automated correctness reasoning for large-scale software. On multiple large systems generated by leading coding agents from Anthropic, NVIDIA, and others, with individual systems up to 143K lines of code, FM-Agent reported 522 potential bugs. These bugs were not detected by unit testing, differential testing, or multi-agent cross review. This talk will present the latest progress of FM-Agent and share practical experience with compilers, databases, and other systems."
    },
    "bio": {
      "zh": "王肇国，上海交通大学教授，博士生导师，重点研发计划项目负责人，国家优秀青年科学基金获得者。从事系统软件研究，成果发表在OSDI、SIGMOD、PODC等相关领域权威会议上。发表ACM通讯（Communications of the ACM）亮点论文和封面文章，并获2023 ACM SIGMOD研究亮点奖、SIGMOD 2022最佳论文优胜奖、CCF青年科技奖、ACM ChinaSys新星奖、华为奥林帕斯先锋奖，以及两次华为火花奖。学术兼职包括OpenHarmony技术指导委员会智能数据管理TSG负责人、ACM ChinaSys秘书长、CCF学术工作委员会委员等。曾受邀担任MLSys 2026、EuroSys 2026/2025、NSDI 2024、SoCC 2024/2023等国际会议的程序委员会成员，以及第22期秀湖论坛联合主席等。",
      "en": "Zhaoguo Wang is a Professor and doctoral supervisor at Shanghai Jiao Tong University. He is a project leader of the National Key R&D Program of China and a recipient of the Excellent Young Scientists Fund of the National Natural Science Foundation of China. His research focuses on system software, with results published in leading venues such as OSDI, SIGMOD, and PODC. His work has appeared as a Research Highlight and cover article in Communications of the ACM. He received the 2023 ACM SIGMOD Research Highlights Award, the SIGMOD 2022 Best Paper Runner-Up Award, the CCF Young Scientist Award, the ACM ChinaSys Rising Star Award, the Huawei OlympusMons Pioneer Award, and two Huawei Spark Awards. He also serves as the leader of the Intelligent Data Management TSG of the OpenHarmony Technical Steering Committee, Secretary-General of ACM ChinaSys, and a member of the CCF Academic Working Committee. He has served on the program committees of MLSys 2026, EuroSys 2026/2025, NSDI 2024, and SoCC 2024/2023, and as a co-chair of the 22nd Xiuhu Forum."
    }
  },
  "yanhong-fan": {
    "id": "yanhong-fan",
    "name": {
      "zh": "樊燕红",
      "en": "Yanhong Fan"
    },
    "aff": {
      "zh": "山东大学",
      "en": "Shandong University"
    },
    "photo": "assets/speakers/yanhong-fan.jpg",
    "title": {
      "zh": "对称密码的自动化分析与设计技术",
      "en": "对称密码的自动化分析与设计技术"
    },
    "abstract": {
      "zh": "对称密码的自动化分析与设计，是突破传统手工推导效率与规模瓶颈的核心路径，也是当前密码学领域最具挑战性的前沿方向之一。本次报告将系统梳理我们在此方向上的核心进展。内容涵盖：密码算法结构特征的自动化表征与理解、基于约束求解（SAT/SMT）的差分、线性及积分区分器的高效搜索方法、面向密码电路面积与时延的多目标优化设计，以及抗侧信道掩码方案的自动生成与评估。此外，我们还将展示自主研发的密码算法自动化测评平台，该平台已实现从分析到设计、从理论到工程的支撑。系列成果发表于EUROCRYPT、FSE、CHES等国际密码学顶级会议，并已在国家关键领域获得实际部署应用。",
      "en": "对称密码的自动化分析与设计，是突破传统手工推导效率与规模瓶颈的核心路径，也是当前密码学领域最具挑战性的前沿方向之一。本次报告将系统梳理我们在此方向上的核心进展。内容涵盖：密码算法结构特征的自动化表征与理解、基于约束求解（SAT/SMT）的差分、线性及积分区分器的高效搜索方法、面向密码电路面积与时延的多目标优化设计，以及抗侧信道掩码方案的自动生成与评估。此外，我们还将展示自主研发的密码算法自动化测评平台，该平台已实现从分析到设计、从理论到工程的支撑。系列成果发表于EUROCRYPT、FSE、CHES等国际密码学顶级会议，并已在国家关键领域获得实际部署应用。"
    },
    "bio": {
      "zh": "樊燕红，山东大学副研究员，密码与数字经济安全全国重点实验室核心成员，长期从事对称密码算法设计及安全防护的相关研究。近五年，承担国家重点研发计划课题等国家级项目及国防任务近10项，在国际密码五大顶会FSE、CHES等发表论文18篇，其中第一作者或通讯作者11篇；申请发明专利14项，已授权8项。研究成果获山东省科学技术发明一等奖、华为“火花奖”、以及全国密码算法设计竞赛一等奖等多项。"
    }
  }
};

const modal = document.getElementById("speaker-modal");
const modalBody = document.getElementById("speaker-modal-body");
const modalClose = document.getElementById("speaker-modal-close");
let lastFocusedElement = null;

function closeNavigation() {
  body.classList.remove("nav-open");
  navToggle?.setAttribute("aria-expanded", "false");
}

navToggle?.addEventListener("click", () => {
  const expanded = navToggle.getAttribute("aria-expanded") === "true";
  body.classList.toggle("nav-open", !expanded);
  navToggle.setAttribute("aria-expanded", String(!expanded));
});

navLinks.forEach((link) => {
  link.addEventListener("click", closeNavigation);
});

function locale() {
  return document.documentElement.lang.startsWith("en") ? "en" : "zh";
}

function textFor(value) {
  if (!value) return "";
  if (typeof value === "string") return value;
  const lang = locale();
  return value[lang] || value.zh || value.en || "";
}

function labels(kind) {
  if (kind === "panel") {
    if (locale() === "en") {
      return { title: "Panel Topic", abstract: "Panelists", bio: "Host Bio" };
    }
    return { title: "Panel 主题", abstract: "嘉宾", bio: "主持人简介" };
  }
  if (locale() === "en") {
    return { title: "Talk Title", abstract: "Abstract", bio: "Speaker Bio" };
  }
  return { title: "报告题目", abstract: "摘要", bio: "报告人简介" };
}

function appendTextBlock(parent, className, text) {
  const block = document.createElement("div");
  block.className = className;
  const parts = String(text || "").split(/\n{2,}/).map((part) => part.trim()).filter(Boolean);
  if (parts.length <= 1) {
    block.textContent = text || "";
  } else {
    parts.forEach((part) => {
      const paragraph = document.createElement("p");
      paragraph.textContent = part;
      block.append(paragraph);
    });
  }
  parent.append(block);
}

function appendLabel(parent, text) {
  const label = document.createElement("div");
  label.className = "speaker-modal-label";
  label.textContent = text;
  parent.append(label);
}

function renderSpeaker(sid) {
  const speaker = SPEAKERS[sid];
  if (!speaker || !modalBody) return;
  const l = labels(speaker.kind);
  modalBody.replaceChildren();

  const inner = document.createElement("div");
  inner.className = "speaker-modal-inner";

  const photo = document.createElement("img");
  photo.className = "speaker-modal-photo";
  photo.src = speaker.photo;
  photo.alt = textFor(speaker.name);
  inner.append(photo);

  const content = document.createElement("div");
  content.className = "speaker-modal-content";

  const name = document.createElement("div");
  name.id = "speaker-modal-name";
  name.className = "speaker-modal-name";
  name.textContent = textFor(speaker.name);
  content.append(name);

  const aff = document.createElement("div");
  aff.className = "speaker-modal-aff";
  aff.textContent = textFor(speaker.aff);
  content.append(aff);

  appendLabel(content, l.title);
  appendTextBlock(content, "speaker-modal-title", textFor(speaker.title));

  appendLabel(content, l.abstract);
  appendTextBlock(content, "speaker-modal-text", textFor(speaker.abstract));

  appendLabel(content, l.bio);
  appendTextBlock(content, "speaker-modal-text", textFor(speaker.bio));

  inner.append(content);
  modalBody.append(inner);
}

function openSpeaker(sid) {
  if (!modal) return;
  renderSpeaker(sid);
  closeNavigation();
  lastFocusedElement = document.activeElement;
  modal.hidden = false;
  modal.setAttribute("aria-hidden", "false");
  body.classList.add("modal-open");
  modalClose?.focus();
}

function closeModal() {
  if (!modal || modal.hidden) return;
  modal.hidden = true;
  modal.setAttribute("aria-hidden", "true");
  body.classList.remove("modal-open");
  lastFocusedElement?.focus?.();
}

document.addEventListener("click", (event) => {
  const opener = event.target.closest("[data-speaker-open]");
  if (opener) {
    openSpeaker(opener.dataset.speakerOpen);
    return;
  }

  const row = event.target.closest("tr[data-sid]");
  if (row) {
    openSpeaker(row.dataset.sid);
    return;
  }

  const card = event.target.closest(".talk-card[data-sid]");
  if (card) {
    openSpeaker(card.dataset.sid);
  }
});

modalClose?.addEventListener("click", closeModal);
modal?.addEventListener("click", (event) => {
  if (event.target === modal) closeModal();
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeNavigation();
    closeModal();
  }
}, true);

function updateActiveLink() {
  const marker = window.scrollY + (header?.offsetHeight ?? 0) + 120;
  let activeHref = "#home";

  navTargets.forEach(({ href, section }) => {
    if (href === "#home") return;
    if (section.offsetTop <= marker) {
      activeHref = href;
    }
  });

  navLinks.forEach((link) => {
    link.classList.toggle("active", link.getAttribute("href") === activeHref);
  });
}

window.addEventListener("scroll", () => {
  if (!header) return;
  header.classList.toggle("is-scrolled", window.scrollY > 16);
  updateActiveLink();
});

window.addEventListener("load", updateActiveLink);
updateActiveLink();
