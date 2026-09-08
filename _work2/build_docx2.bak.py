# -*- coding: utf-8 -*-
"""
Capabilities and Fundamental Limits of Latent Chain-of-Thought —— 中文翻译版 Word 文档生成器
正文使用宋体(SimSun)，插图/定理/公式以高清图片嵌入，保持与原论文相同位置。
"""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

WORK = r"D:\论文\_work2"
FIG = os.path.join(WORK, "media")
MATH = os.path.join(WORK, "math")
OUT_DIR = r"D:\论文\zh_cn"
os.makedirs(OUT_DIR, exist_ok=True)

CN_FONT = "宋体"
EN_FONT = "Times New Roman"

doc = Document()

def set_run_font(run, size=10.5, bold=False, italic=False, color=None, cn=CN_FONT, en=EN_FONT):
    run.font.name = en
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), en)
    rFonts.set(qn('w:hAnsi'), en)
    rFonts.set(qn('w:eastAsia'), cn)
    rFonts.set(qn('w:cs'), en)

def add_para(text, size=10.5, bold=False, italic=False, align=None,
             space_after=5, space_before=0, indent=None, cn=CN_FONT,
             color=None, line=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    if line is not None:
        pf.line_spacing = line
    if indent is not None:
        pf.first_line_indent = Pt(indent)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic, color=color, cn=cn)
    return p

def add_heading(text, level=1):
    size = {1: 14, 2: 12, 3: 11}.get(level, 11)
    return add_para(text, size=size, bold=True, space_before=10, space_after=6, color=RGBColor(0,0,0))

def add_image(path, width_in=6.3, center=True):
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(8); pf.space_after = Pt(4)
    run = p.add_run()
    run.add_picture(path, width=Inches(width_in))
    return p

def add_caption(text, size=9):
    return add_para(text, size=size, align=WD_ALIGN_PARAGRAPH.CENTER,
                    space_after=10, space_before=2)

def add_math(path, width_in=4.0):
    """Embed a theorem/equation image, centered."""
    return add_image(path, width_in=width_in)

def add_labeled_para(label, text, size=10.5):
    """Paragraph starting with a bold lead-in label (e.g., 'CoT模型...')."""
    # Reproduce by a normal paragraph; the bold lead-in is a minor stylistic choice.
    return add_para(text, size=size, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=5)

# ===== 页面设置 =====
sec = doc.sections[0]
sec.left_margin = Inches(1.0)
sec.right_margin = Inches(1.0)
sec.top_margin = Inches(0.9)
sec.bottom_margin = Inches(0.9)

# ===== 标题 =====
add_para("潜思维链的能力与根本局限", size=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
add_para("（英文原标题：Capabilities and Fundamental Limits of Latent Chain-of-Thought）",
         size=9, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10, color=RGBColor(0x66,0x66,0x66))
add_para("Jiaxuan Zou *¹   Yaozhong Xiong *²   Yong Liu ²", size=11,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_para("¹西安交通大学数学与统计学院，陕西西安 710049；²中国人民大学高瓴人工智能学院，北京 100872。通讯作者：Yong Liu <liuyonggsai@ruc.edu.cn>。",
         size=9, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
add_para("*共同一作。", size=9, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6,
         color=RGBColor(0x66,0x66,0x66))
add_para("arXiv:2602.01148v1  [cs.AI]  2026年2月1日", size=9, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_after=12, color=RGBColor(0x44,0x44,0x44))

# ===== 摘要 =====
add_heading("摘要", level=1)
abstract = ("潜思维链（Latent Chain-of-Thought，Latent CoT）模型承诺通过连续表示实现高效推理，却暴露出令人困惑的性能不一致："
            "在探索类任务（ProsQA：97.0%）上表现优异，却在计算类任务（GSM8K：34.1%）上失败。我们发现这一权衡由「决策确定性」"
            "所支配。我们的贡献有三个方面：（1）理论上刻画了根本性的「探索—执行权衡」，证明高确定性带来精确执行却抑制探索，"
            "低确定性则促进搜索却导致误差累积。（2）我们引入了「符号指数」（Symbolic Index）——用以量化决策承诺——作为支配这一"
            "权衡的核心机制，并确立了它与执行稳定性及探索能力之间的因果关系。（3）我们证明课程学习在理论上是必要的，因为直接训练"
            "会因分布失配而必然失败。我们的框架把设计范式从二元的架构选择，转向根据任务需求动态调节决策确定性的自适应系统。")
add_para(abstract, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

intro_p = ("潜思维链模型承诺通过连续表示实现高效推理，却在实验性能上呈现出一种尖锐而令人困惑的二律背反。"
           "如表1 所示，显式思维链（Explicit CoT）与潜思维链（Latent CoT）表现出互补、甚至互斥的失败模式。"
           "显式 CoT 在需要精确符号操作与严格逻辑执行的任务上表现出色，例如 GSM8K 中的算术推理（42.9% 准确率）。"
           "然而，它在需要灵活探索或策略规划的任务上却明显吃力，例如 ProsQA（77.5%），常常过早地固守一条僵化路径。"
           "相反，潜思维链在探索性任务上取得更优性能（97.0%），借助其连续表示遍历更广的搜索空间。然而，这种灵活性伴随着"
           "严重代价：潜思维链在精度至关重要的计算类任务上灾难性地失败，因为这类任务需要精确的状态维护。此外，潜思维链表现出"
           "极端的训练脆弱性；正如消融结果所示，移除课程学习会导致性能崩塌（例如在 ProntoQA 上从 99.8% 跌到 52.4%），"
           "表明这些模型学习推理的方式存在根本性不稳定。")
add_para(intro_p, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 1 引言 =====
add_heading("1  引言", level=1)
p1 = ("大型语言模型（LLM）的出现（Guo et al., 2025; OpenAI, 2025; DeepSeek-AI, 2025）标志着人工智能的一次范式转变，"
      "从根本上重塑了复杂推理任务的版图（Liu et al., 2025）。迄今为止，激发推理能力的主导方法一直是显式思维链（CoT）"
      "（Wei et al., 2022; Sun et al., 2023）。通过迫使模型把中间步骤以离散词元的方式表达出来，CoT 强加了一种结构化、"
      "人类可读的逻辑流，从而显著提升性能。然而，这种显式")
add_para(p1, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
# 右栏文本（第1页右侧，承接上一段）
p1b = ("表达（verbalization）代价高昂：由于过长的序列长度以及自回归瓶颈带来的计算负担，它固有地效率低下"
       "（Hong et al., 2025; Yue et al., 2025）。为应对这些可扩展性局限，近期研究已激进地转向「隐式推理」，通常称为潜思维链"
       "（Ye et al., 2025）。在此范式中，模型在连续的内部状态空间中运行，通过「无声」的向量变换处理信息，而不生成中间词元。"
       "借助词元级操作（Tack et al., 2025; Sun et al., 2025）与轨迹优化（Cheng & Van Durme, 2024; Hao et al., 2024a）等机制，"
       "这些模型承诺降低计算复杂度，并解锁更多样、更高维、不受自然语言词汇约束的推理路径（Hao et al., 2024a; Zhang et al., 2025a）。")
add_para(p1b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p1c = ("尽管有这些架构创新，实验性能中仍浮现出一种尖锐而令人困惑的二分。正如表1 所示，显式 CoT 与潜思维链表现出互补、"
       "甚至互斥的失败模式。显式 CoT 在需要精确符号操作与严格逻辑执行的任务上表现优异，例如 GSM8K 的算术推理（42.9% 准确率）；"
       "然而它在需要灵活探索或策略规划的任务上（如 ProsQA，77.5%）明显吃力，常常过早固守一条僵化路径。相反，潜思维链在探索性"
       "任务上取得更优性能（97.0%），凭借其连续表示遍历更广的搜索空间。然而，这种灵活性带来严重惩罚：潜思维链在精度要求极高的"
       "计算类任务上灾难性地失败，而这类任务中的精确状态维护至关重要。此外，潜思维链表现出极端的训练脆弱性；正如消融结果所示，"
       "移除课程学习导致性能崩溃（例如在 ProntoQA 上从 99.8% 跌到 52.4%），表明这些模型学习推理的方式存在根本性不稳定。")
add_para(p1c, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p1d = ("这些实证观察凸显了我们在理论理解上的一个关键缺口。目前，该领域缺乏一个统一框架来解释：为什么在探索上的高性能必须以牺牲"
       "执行精度为代价，以及为什么隐式模型本质上难以训练。现有文献大多把这些架构视为二元的——离散对连续——而没有刻画支配它们各自"
       "优点与弱点的底层决策理论机制。因此，当前的架构设计依赖启发式，而非对模型内部推理过程进行有原则的调节，导致系统要么精确"
       "但僵化，要么灵活但充满幻觉。")
add_para(p1d, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p1e = ("本文提出，这种权衡并非架构的任意产物，而是决策确定性的根本结果。我们引入「符号指数」（Symbolic Index）——一种衡量"
       "模型对特定推理路径承诺程度的可量化指标——作为统摄这些现象的核心机制。我们的关键洞见是：显式 CoT 运行在高确定性区间。"
       "该区间通过纠错的离散化过程（对特定词元的选择）保证计算保真度，但会因过早固守单一轨迹而坍缩探索。相反，潜思维链运行在"
       "低确定性区间，维持对多条推理路径的叠加。尽管这种叠加使我们能对复杂解空间进行稳健探索，但它饱受噪声累积之苦，最终摧毁"
       "符号精度，因为没有离散量化步骤来重置内部状态。")
add_para(p1e, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p1f = ("我们的贡献有三个方面。首先，我们理论上刻画了根本性的「探索—执行权衡」。我们证明 CoT 的高决策确定性会导致探索消失，"
       "而潜思维链的低确定性会放大次决策噪声，成为算术任务上失败的直接原因。其次，我们形式化了「符号指数」这一调节指标，为下一代"
       "能够在探索与执行之间动态切换的架构提供了具体的设计原则。第三，我们解决了训练稳定性之谜，证明课程学习对潜思维链在理论上是"
       "必要的。我们证明，没有课程，训练必然失败，原因是模型自生成的潜在状态与有效推理轨迹之间存在分布失配——而课程恰好弥合了这一"
       "鸿沟。")
add_para(p1f, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 表1 =====
add_image(os.path.join(FIG, "table1.png"), width_in=6.3)
add_caption("表1：离散（CoT）与潜在（Coconut）推理模型的性能揭示出令人困惑的权衡。CoT 在精确计算（GSM8K）上表现出色，"
            "但在灵活推理（ProsQA）上吃力。相反，潜思维链擅长灵活性，却在计算上失败，且对其训练课程高度敏感。*结果取自（Hao et al., 2024b）。",
            size=9)

# ===== 2 相关工作 =====
add_heading("2  相关工作", level=1)
p2a = ("与受限在单一离散路径上的显式 CoT 不同，潜思维链借助连续潜在空间实现探索性多样化。这一领域的研究使模型能够并行探索多条"
       "推理轨迹，从而增强在复杂问题上的鲁棒性。相关技术包括：采样潜在轨迹（Chen et al., 2024）、使用概率加权概念（Zhang et al., 2025b）、"
       "以及注入连续词元以丰富搜索空间（Xu et al., 2025b;a; Gozeten et al., 2025）。这些实证成功证明了探索能力的价值。"
       "我们把这一直觉形式化：证明探索能力源于维持较低的决策确定性——即较低的符号指数——并确立与理想均匀探索先验之间 KL 散度的"
       "形式上界（定理4.5）。")
add_para(p2a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p2b = ("另一条研究脉络聚焦于轨迹级的潜在优化，把整条显式推理链压缩为连续表示。早期工作旨在通过把潜在状态锚定到显式步骤来保持"
       "语义保真度（Cheng & Van Durme, 2024; Liu et al., 2024; Shen et al., 2025b）。更近的工作通过动态压缩或自适应控制来提升效率"
       "（Zhang et al., 2025a; Ma et al., 2025; Tan et al., 2025; Wang et al., 2025a）。一个尤其重要的策略是渐进式内化"
       "（progressive internalization），即通过课程学习（Deng et al., 2024; Hao et al., 2024a; Shen et al., 2025a）或内部迭代"
       "（Zeng et al., 2025; Ruan et al., 2025），逐步用潜思维替代显式步骤。这些方法——尤其是那些使用课程的方法——为我们的分析提供"
       "了实证动机。我们的工作补充这些实证发现：我们证明渐进式训练不仅有益，而且在理论上必要，以克服根本性的分布失配（定理5.1）"
       "并确保收敛（定理5.2，第5节）。")
add_para(p2b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p2c = ("除了这些架构进步，一条并行研究脉络探索对内部状态的细粒度控制与分析。信号引导的控制方法插入专门的、不产生文本的词元来"
       "引导内部推理（Herel & Mikolov, 2024; Goyal et al., 2024; Zelikman et al., 2024; Pfau et al., 2024; Wang et al., 2024）。"
       "与此同时，内部状态分析利用探针（probing）或蒸馏等技术寻找隐式推理的机制性证据，例如在注意力模式中发现编码好的推理树"
       "（Deng et al., 2023; Hou et al., 2023; Wang et al., 2025b; Yu et al., 2024）。这两种方法都凸显了内部状态的核心地位。"
       "我们通过证明「内部确定性的方差」是探索—执行权衡的根本原因（定理4.11 与 4.12，第4.4节），统一了这些机制性洞见。"
       "我们的符号指数为这些原本难以名状的内部状态提供了一个可计算、可量化的指标，也为未来的架构创新提供了有原则的评价标准。")
add_para(p2c, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 3 预备知识 =====
add_heading("3  预备知识", level=1)
p3a = ("我们考虑推理任务的监督学习，其中输入是随机变量 X，实例 x 从中抽取。每个输入 x 与答案 y 由一条思维链 "
       "S = (s_1, …, s_M) 相连。我们比较两种建模该过程的范式：思维链（CoT）与潜思维链（Latent CoT），后者通过 Coconut 课程训练。")
add_para(p3a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("思维链（CoT）：CoT 模型自回归地生成离散推理步骤：", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_cotp.png"), width_in=4.2)
p3b = ("在推理时，词元选择会固守单一路径——从而能进行精确计算，但会冒早期出错的风险"
       "（Mohtashami et al., 2025; Yu et al., 2025; Xu et al., 2024; Emmons et al., 2025）。")
add_para(p3b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("潜思维链（Latent CoT）：潜思维链在连续空间中迭代，产生潜在状态 H = (h_1, …, h_M)，h_k ∈ ℝ^d：",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_latent.png"), width_in=3.0)
p3c = ("每个 h_k 编码了多条潜在推理路径，支持探索，但随着步数推移会累积噪声（Kong et al., 2025; Zhu et al., 2025; Su et al., 2025; Orlicki, 2025）。")
add_para(p3c, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("Coconut 训练（Hao et al., 2024b）：由于对 H 的直接监督不可行，Coconut 采用课程。在第 k 阶段，它学习把前缀 "
         "S^(1…k) 压缩为潜在状态 h_k，以预测后缀 S^(k+1…M)：", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_coconut.png"), width_in=4.0)
p3d = ("该课程从 k = 0（纯 CoT）推进到 k = M（全潜推理），逐步内化那些衔接离散与连续 CoT 的符号步骤。")
add_para(p3d, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

# ===== 4 理论分析 =====
add_heading("4  理论分析", level=1)
p4a = ("本节对 CoT 与潜思维链之间的根本差异与权衡进行深入的理论分析。我们首先透过信息瓶颈（Information Bottleneck）理论的视角，"
       "揭示 Coconut 训练目标的数学基础。随后，我们沿两个关键维度直接分析模型性能：规划与探索能力，以及计算执行精度。最后，"
       "我们确定以符号指数量化的决策确定性是调节这一权衡的核心机制，并理论上确立课程学习对有效训练潜思维链模型的必要性。")
add_para(p4a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("4.1  与信息瓶颈的对偶性", level=2)
p411 = ("直接分析 Coconut 训练模型的行为颇具挑战，因为其目标是分阶段、隐式的压缩。为克服这一点，我们证明 Coconut 课程在数学上"
        "等价于求解一个研究较充分的信息论目标——条件信息瓶颈（Conditional Information Bottleneck）（Tishby & Zaslavsky, 2015）。"
        "这一等价使我们能借助信息论的既有工具，严格刻画模型的性质。")
add_para(p411, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p411b = ("这一对偶性可以直观理解：Coconut 目标在第 k 阶段所提出的，是一个信息压缩问题。模型必须把过去的思维链 S^(1…k) 压缩为"
         "单一潜在向量 h_k，其唯一目的是最大化它对预测未来链 S^(k+1…M) 的效用。这恰恰是信息瓶颈（IB）原理所解决的问题："
         "为「源」（过去）寻找一个压缩的「瓶颈」表示，同时形式上保留关于「目标」（未来）的信息。Coconut 的训练过程因此隐式地"
         "学习了一个最优信息压缩器。定理4.1 把这一直觉形式化。")
add_para(p411b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("定理4.1（Coconut–CIB 对偶性）：在任意有限模型容量的约束下，Coconut 课程在第 k 阶段的优化目标（预备知识3）可以被严格"
         "重述为一个约束优化问题。它的拉格朗日对偶正是条件信息瓶颈（CIB）问题。具体而言：", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_primal.png"), width_in=4.6)
add_para("其中 β(k) > 0 理想地满足 β(k) ~ k / (M − k)。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("β(k) 的解读：", size=10.5, bold=True)
add_para("权衡参数 β(k) ~ k/(M − k) 反映了课程在不同阶段的重点转移。随着 k 增大，模型压缩更多过去信息，同时保持对较短未来序列的"
         "预测能力，从而动态地平衡压缩效率与预测效用。这种动态加权确保了每个阶段的最优平衡；我们把训练的必要性形式化于 §5。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p411c = ("主要挑战在于把 Coconut 的操作训练损失与一个正式的信息论目标联系起来。证明通过把优化建构为一个约束问题并应用"
         "拉格朗日对偶性来完成，从而揭示 Coconut 隐式求解的是条件信息瓶颈。证明见附录 A.2。")
add_para(p411c, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("4.2  潜思维链在探索上的优势", level=2)
p42a = ("我们把推理建模为对决策有向无环图（DAG）Q := (G, v_start, V_target) 的遍历。在任意节点 v 处，令 N_valid(v) 为有效后继步骤的"
        "集合。一个理想的探索者使用均匀先验 q_PR(u | v) = (1/|N_valid(v)|)·1[u ∈ N_valid(v)]。我们通过 D_KL(q_PR‖p) 衡量与此理想的"
        "偏离，其中 p 是模型的后继步骤分布：KL 散度低意味着广泛探索；KL 散度高则意味着过度自信与过早承诺。")
add_para(p42a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p42b = ("我们的分析首先聚焦于单一、连贯的推理路径的固有属性，它构成了 CoT 范式的基本构件。理解这样一条轨迹的生成过程，对于剖析"
        "执行的核心机制至关重要。为使这一过程形式化，我们刻画 CoT 在成功推理期间表现出的高确定性行为。这并非任意的建模选择，"
        "而是 CoT 在确定性推理链上通过教师强制（teacher-forcing）训练的内在结果，后者自然地诱导出尖峰分布。")
add_para(p42b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("假设4.2（CoT 的 κ 集中分布）：在具有 B 个选项的决策点上，我们把单步 CoT 的生成分布 p_CoT 建模为来自具有大集中参数 "
         "κ = Σ_i α_i 的狄利克雷（Dirichlet）先验。大的 κ 产生尖峰分布，反映出确定性、高保真执行所需的高决策确定性。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("在此假设下，CoT 必然在每一步坍缩其分布：", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_para("定理4.3（CoT 的探索不足）：当 κ → ∞ 时，熵 H(p_CoT) → 0，且", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_dkl4_2.png"), width_in=4.6)
add_para("证明见附录 A.3。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("注4.4（基于采样的方法）：我们的分析支配的是单条推理链的生成。虽然集成方法（如自洽性，Self-Consistency，"
         "Wang et al., 2023）通过采样多条链引入探索，但每条链自身的计算完整性仍取决于定义 CoT 以执行为核心的高确定性承诺。"
         "因此，我们的核心结果依然具有根本性。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p423 = ("这量化了 CoT 在 ProsQA 等探索性任务上的糟糕表现（表1 中 77.5% 对潜思维链的 97.0%）：散度 D_KL → ∞ 形式化了 CoT 的分布"
        "变得与均匀探索先验任意远。")
add_para(p423, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("相比之下，潜思维链的训练目标——对条件信息瓶颈对偶（定理4.1）——施加了针对过度自信的隐式正则化，确保持续的探索：",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_para("定理4.5（潜思维链的探索能力保证）：存在常数 δ ∈ (0, 1) 与有限的 c，使得", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_thm45.png"), width_in=4.0)  # DKL upper bound (Thm 4.5)
add_para("证明见附录 A.4。这一 D_KL 的有限上界确保潜思维链维持一个非退化的选项分布，与 CoT 的无界散度（定理4.3）形成鲜明对比。"
         "这保证了稳健的探索，补充了 CoT 在执行上的优势，我们接下来分析后者。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("4.3  潜思维链在符号计算上的脆弱性", level=2)
p43a = ("虽然潜思维链的连续状态空间支持稳健探索（第4.2节），但它对需要高保真符号推理的任务（如 GSM8K）而言是一种负担。与 CoT 的"
        "离散符号操作不同，潜思维链的连续状态表示天然易受噪声累积影响，这会破坏逐步的精确计算。")
add_para(p43a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p43b = ("为使这一点形式化，我们分析小的内部误差的效果，称之为「次决策扰动」（sub-decisional perturbations）——指那些破坏模型"
        "内部状态、但又不足以改变即时输出的噪声。")
add_para(p43b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("定义4.6（次决策扰动）：令 l_k = l*_k + ϵ_k 为第 k 步的逻辑向量。若", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_def46.png"), width_in=3.2)
add_para("则扰动 ϵ_k 是次决策的。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p43c = ("这一概念凸显出关键的架构分歧。由于其离散的生成过程，CoT 模型对这些扰动天然鲁棒。")
add_para(p43c, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("定理4.7（CoT 的符号完整性）：令 S* = (s*_1, …, s*_M) 为无噪声的 CoT 轨迹，Ŝ 为次决策扰动下的轨迹，则",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_thm47.png"), width_in=2.4)
add_para("证明见附录 A.5。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p43d = ("定理4.7 形式化了 CoT 对次决策扰动的韧性。其底层机制是「离散化重置」过程：每一步的 argmax 操作都充当一个纠错滤波器，"
        "把连续隐藏状态投影为离散词元，从而丢弃任何次决策噪声。这种重置确保后续推理从干净的符号表示开始，防止误差在推理链中传播。")
add_para(p43d, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p43e = ("与此形成鲜明对比的是，潜思维链缺乏这种离散化重置机制。其连续状态 h_k 未经量化直接传到下一步，把任何扰动都携带着向前传播。"
        "对于一个具有转移函数 f_θ（利普希茨常数 L_F）与独立同分布噪声 ϵ_h^(k) ~ N(0, σ²_h I_d) 的模型，这种误差传播是可量化的：")
add_para(p43e, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_para("定理4.8（潜计算中的复合误差）：令 E_M = h_M − h*_M。则对于 M ≥ 1，", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_thm48.png"), width_in=3.4)
add_para("证明见附录 A.6。项 (1 − L_F^{2M})/(1 − L_F²) 表明期望平方误差随推理步数 M 增长。如果模型的转移函数是扩张的（L_F > 1），"
         "误差呈指数复合；即使对稳定函数（L_F ≤ 1），误差仍然累积。这一数学结果直接解释了潜思维链在 GSM8K 这类精度敏感任务上的"
         "性能退化。即使是很小的扰动，在长推理链上累积起来也会破坏最终状态，损害符号计算所需的完整性，并与第4.2节分析的两分相补充。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("4.4  通过符号指数统一权衡", level=2)
p44a = ("第4.2节与第4.3节的分析揭示了一种二分：CoT 擅长执行但缺乏探索，而潜思维链则相反。这里，我们通过一个单一、可量化的原理"
        "——每一步推理的决策确定性程度——来统一这些行为。为使这一点形式化，我们引入符号指数（I_S），一种衡量模型对其最佳选择承诺"
        "程度的指标。")
add_para(p44a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("定义4.9（符号指数 I_S）：在具有有效词元词汇 V 的决策点上，令 p(u | h, x) 为模型的输出分布。符号指数是最可能词元的概率：",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_def49.png"), width_in=3.2)
add_para("高的 I_S（≈1）表示高确定性，是 CoT 离散承诺的特征。低的 I_S 表示对多个选项的分布式考虑，是潜思维链的特征。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p44b = ("首先，我们建立这种确定性与对计算噪声的鲁棒性之间的直接联系。这种鲁棒性的机制是前两个选择之间的分隔，我们称之为"
        "「逻辑决策裕度」（Logit Decision Margin）。")
add_para(p44b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("定义4.10（逻辑决策裕度 Δl）：令 l*_i 与 l*_j 分别是最可能词元与第二可能词元的逻辑值。裕度是它们的差：Δl = l*_i − l*_j。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p44c = ("下面的定理证明高确定性保证大的决策裕度，使模型对扰动具有韧性。")
add_para(p44c, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_para("定理4.11（符号稳定性定理）：逻辑决策裕度 Δl 以符号指数 I_S 为下界，具体如下：", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_thm411.png"), width_in=3.2)
add_para("证明见附录 A.8。该定理确立了直接关系：更高的决策确定性保证更大的保护裕度。例如，具有 I_S = 0.99 的高确定性 CoT 的裕度 "
         "Δl ≥ log(99) ≈ 4.6，使其决策对显著噪声鲁棒。相反，具有 I_S = 0.6 的低确定性潜思维链只有 Δl ≥ log(1.5) ≈ 0.4 的裕度，"
         "使其易受微小扰动影响。这解释了 CoT 的噪声免疫与符号完整性（定理4.7）。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p44d = ("然而，这种稳定性给探索带来了直接且可量化的代价。高确定性迫使模型的分布远离无偏探索所要求的均匀理想。下一个定理形式化"
        "这种权衡。")
add_para(p44d, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_para("定理4.12（探索—执行权衡定理）：对于具有 B 个有效选项的决策，与理想均匀探索先验 q_PR 的 KL 散度以下式为下界：",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_thm412.png"), width_in=4.2)
add_para("该下界在 I_S = 1/B 时最小，并随 I_S → 1 而增大。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("证明见附录 A.9。这一不等式证明：通过增大 I_S 获得执行稳定性，必然通过增大与均匀策略的散度而损害探索能力。它量化了"
         "「固守单一路径」与「保持选项开放」之间的内在张力，解释了 CoT 的探索不足（定理4.3）。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p44e = ("综上，这些结果确立了 I_S 作为核心调节器，统摄两种范式：")
add_para(p44e, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_para("1. CoT：高 I_S 区间确保大的决策裕度以实现稳健执行（定理4.11、4.7），但损害探索（定理4.12）。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=3, indent=18)
add_para("2. 潜思维链：低 I_S 区间实现广泛探索（定理4.5），但意味着小的决策裕度，导致易受逐步复合的次决策噪声影响"
         "（定理4.8），进而在精度敏感的任务上失败。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, indent=18)
p44f = ("这一框架把焦点从二元的架构选择，转向管理决策确定性，暗示了根据任务需求动态调节 I_S 的自适应系统。")
add_para(p44f, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

# ===== 5 为什么课程学习有效 =====
add_heading("5  为什么课程学习有效", level=1)
p5a = ("在确立 I_S 支配训练后模型的探索—执行权衡（§4.4）之后，我们现在面对一个根本问题：我们如何训练一个模型在低 I_S 区间运行，"
       "以进行稳健探索？这揭示了潜思维链训练固有的一种悖论。与每步都受益于词元级监督的显式 CoT 不同，潜思维链必须学习生成"
       "有意义的潜在表示 h_k，却没有显式的真值。")
add_para(p5a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("5.1  潜思维链的训练悖论", level=2)
p51a = ("一个未经训练的模型没有动力去执行 h_k 中编码的多步推理；相反，它倾向于学习「捷径」表示，仅仅把表层输入模式映射为输出。"
        "训练需要可靠的梯度信号，而这需要高确定性（高 I_S）预测来最小化损失方差。然而，最终目标却是学习支持探索的低 I_S 表示。"
        "直接训练因此把模型困在高 I_S 区间，阻碍了真正潜在推理的涌现。")
add_para(p51a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p51b = ("为严格分析这一困难，我们在模仿学习（Imitation Learning，IL）框架内建模该问题。令 P_θ*(h|x) 为生成最优、编码推理的"
        "潜在状态的不可观测专家策略。我们定义一个二值估值函数 V(h) ∈ {0, 1}，其中 V(h) = 1 表示该潜在状态通向正确答案。"
        "主要目标是最大化任务成功率 R(θ)，定义为——在诱导策略下这一函数的期望：")
add_para(p51b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_R.png"), width_in=3.2)
p51c = ("没有课程，模型必须从自生成的潜在状态学习。这些自生成状态来自表面化表示的偏置分布 P_biased，它从根本上不同于真正的专家分布 "
        "P_θ*。由于估值函数 V(h) 是非均匀的（偏好推理状态），从失配分布学习保证次优性能。")
add_para(p51c, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("定理5.1（无课程训练的可证明失败）：令 D_nc 为从偏置分布 P_biased 抽取的潜在状态数据集。如果该分布相对于专家本质上为次优"
        "（即 R(P_biased) ≤ R(θ*) − Δ，对某个间隙 Δ > 0），那么在 D_nc 上训练的模型 θ̂_MLE 严格有界地偏离最优：",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_thm51.png"), width_in=3.2)
add_para("其中 C(Δ) > 0 是由偏置决定的常数。这意味着模型的成功率被永久封顶在专家的性能之下，无论数据集大小如何。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("证明见附录 A.10。该定理证明在「捷径」潜在状态上训练会把模型锁定在次优策略。不同于随数据消失的方差误差（见定理5.2），"
         "这种偏置误差是不可约的。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("5.2  课程学习作为受控的 I_S 转移", level=2)
p52a = ("从符号指数的视角看，这可以理解为一个受控的转移。在早期阶段（纯 CoT），高 I_S 通过纠错离散化确保准确的词元级梯度。在混合"
        "阶段，前缀在潜在空间（低 I_S）运行，但后缀保留显式词元生成。这把潜在表示锚定到有效的推理轨迹。最终，模型达到探索所需的低 "
        "I_S，并由渐进式内化稳定下来。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p52b = ("在我们的 IL 框架中，这一过程有效地提供了扎根于正确推理的潜思维监督样本，等价于直接从 P_θ*(h|x) 抽样。关键是，分布收敛"
        "保证性能收敛。由于估值函数 V(h) 有界于 [0, 1]，成功率之差 |R(θ̂) − R(θ*)| 以策略之间的总变差（Total Variation）距离为上界。"
        "因此，通过课程学习最小化分布散度，可直接优化任务成功率。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("定理5.2（有课程训练的可证明成功）：在标准统计学习条件下，在大小为 n、通过课程生成的、由专家分布生成的数据集 D_c 上进行 "
         "MLE，得到模型 θ̂，其成功率逼近专家的成功率：", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2)
add_math(os.path.join(MATH, "eq_thm52.png"), width_in=4.4)
add_para("以概率 ≥ 1 − δ。随着数据集大小 n → ∞，性能差距消失。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("证明见附录 A.11。该定理确认：通过使用显式 CoT 作为脚手架来生成有效训练数据，课程确保学生模型可证明地收敛到最优专家策略。"
         "总之，课程学习在理论上是必要的，以解决分布失配（定理5.1）并确保收敛（定理5.2）。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 6 实验 =====
add_heading("6  实验", level=1)
add_para("我们开展实证评估，以验证第4.4节建立的理论框架。我们的实验验证三个假设：（1）潜思维链与显式 CoT 运行在决策确定性的不同区间"
         "（验证定理4.3 与 4.5）；（2）这种确定性差异决定了对计算噪声的鲁棒性（验证定理4.11 与 4.12）；以及（3）潜思维链表现出与"
         "连续状态动力学一致的误差累积（验证定理4.8）。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("实验设定：我们使用 GPT-2（124M）架构。我们把标准的显式 CoT 模型与经由 Coconut 课程（M = 6 个潜步骤）训练的潜思维链模型"
         "对比。评估在 GSM8K（Cobbe et al., 2021，用于精确符号计算）与 ProsQA（Hao et al., 2024b，用于探索性推理）上进行。"
         "实现细节见附录 A.1。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("6.1  决策确定性（I_S）分析", level=2)
p61 = ("为验证探索—执行权衡（定理4.12），我们测量符号指数（I_S），定义为给定步的最大词元概率。图1 与图2 显示了 I_S 值的分布：",
        size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_image(os.path.join(FIG, "fig01.png"), width_in=5.2)
add_caption("图1：GSM8K 上的符号指数。潜思维链（所示）维持较低的符号指数（I_S ∈ [0.2, 0.5]），表明为分散的概率分布。"
            "它缺乏在显式 CoT 中观察到的概率集中（I_S ≈ 1.0）。", size=9)
add_image(os.path.join(FIG, "fig02.png"), width_in=5.2)
add_caption("图2：ProsQA 上的符号指数。潜思维链在推理步骤中表现出稳定、低 I_S 的分布。这验证了定理4.5，表明模型把概率质量"
            "分散到多条潜在路径，而不是收敛到单一词元。", size=9)
p61b = ("• 通过低 I_S 探索（ProsQA）：在 ProsQA 上（图2），潜思维链模型维持 I_S < 0.6。这实证地确认了定理4.5。持续的低 I_S 表明"
        "模型在潜在空间中保留多条潜在推理轨迹，防止过早收敛到次优解。这一机制支持了探索性任务上观察到的 97.0% 高准确率。",
        size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, indent=18)
p61c = ("• 缺乏离散化（GSM8K）：在 GSM8K 上（图1），模型在没有高概率集中的情况下运行（I_S ≪ 1.0）。根据定理4.11，低 I_S 对应"
        "极小的逻辑决策裕度 Δl。与利用「argmax」操作在每个词元处重置状态方差的显式 CoT 不同，潜思维链连续传播方差。缺乏中间误差校正"
        "导致了更低的计算准确率（34.1%）。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, indent=18)

add_heading("6.2  噪声鲁棒性与稳定性分析", level=2)
p62a = ("为验证误差传播（定理4.8）与稳定性界（定理4.11），我们把高斯噪声 N(0, σ²I_d) 注入隐藏状态（潜思维链）或预输出状态（CoT），"
        "并测量精确匹配（Exact Match）准确率的下降。")
add_para(p62a, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p62b = ("图3 中的结果展示了两种不同的失败模式：")
add_para(p62b, size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_image(os.path.join(FIG, "fig03.png"), width_in=5.4)
add_caption("图3：噪声下的性能退化。标准 CoT（橙色）表现出阈值效应：在 σ 超过决策裕度之前性能保持不变。潜思维链（蓝色）从 "
            "σ ≈ 0 开始单调衰减。这与附录 A.7 中的推导 A(σ) = Φ(Δl / √(C)·σ) 一致。", size=9)
p62c = ("• 显式 CoT（阶跃函数响应）：对低噪声，显式 CoT 的准确率曲线保持平坦，在急剧下降前呈现显著平台。这确认了存在非零的逻辑决策"
        "裕度 Δl。对于噪声向量 ‖ϵ‖ < Δl，离散投影（词元选择）有效地过滤掉扰动（定理4.7）。", size=10.5,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, indent=18)
p62d = ("• 潜思维链（连续衰减）：潜思维链表现出立即的单调退化。这确认了在连续潜在表示中 Δl ≈ 0。没有离散裕度，扰动直接改变状态轨迹。"
        "GSM8K 上的衰减速率支持定理4.8，表明转移函数 f_θ 在推理步 M = 6 上累积误差。", size=10.5,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, indent=18)
add_image(os.path.join(FIG, "fig04.png"), width_in=5.4)
add_caption("图4：任务相关的敏感性。在相同的噪声水平下，潜思维链在 ProsQA（橙色）上比在 GSM8K（蓝色）上保持更高的性能。这表明"
            "探索性任务对状态偏移的容忍度大于精确计算任务。", size=9)
p62e = ("图4 显示鲁棒性取决于任务域。虽然 GSM8K 性能快速下降，但 ProsQA 在噪声下相对稳定。这表明探索性任务的解空间是连续的"
        "（h_M 的微小偏差仍映射到有效语义输出），而计算任务要求 h_M 保持在一个狭窄区域内才能产生正确的数值词元。", size=10.5,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("6.3  消融：课程学习", level=2)
p63 = ("我们分析没有课程时潜思维链的训练稳定性（表1：ProntoQA 上 52.4% 准确率）。监测训练过程发现，没有课程，模型在早期 epoch 就收敛"
        "到高 I_S 区间。这产生了分布失配：模型基于输入—输出统计学习一个确定性映射，而非专家潜在策略 P_θ*（定理5.1）。因此，课程对于"
        "强制实施低 I_S 推理能力涌现所需的分布对齐是必要的。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 7 结论 =====
add_heading("7  结论", level=1)
p7a = ("在本工作中，我们引入了符号指数，作为一个统一的理论框架，用以解释语言模型推理中探索与执行之间的根本权衡。我们的分析确定"
        "决策确定性是支配机制：显式 CoT 的高确定性通过纠错离散化保障计算保真度，但因过早承诺而限制探索；而潜思维链的低确定性"
        "促进广泛搜索，却因复合误差而牺牲符号完整性。我们进一步证明，课程学习对潜思维链是理论上的必要，它弥合了本会把模型困在"
        "次优策略中的分布失配，从而确保收敛。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
p7b = ("虽然符号指数目前是诊断性指标，但它揭示了当前范式设计的一个关键局限：决策确定性的僵化。我们的框架表明，推理架构的进步需要"
        "超越离散与连续模态之间的二元选择。相反，未来研究应优先考虑能够动态调节其决策确定性的自适应系统——在用于精确执行的高确定性"
        "承诺与用于规划的低确定性多样化之间调制。通过确立决策确定性作为核心设计原则，本工作为开发能够根据任务需求在严谨计算与灵活"
        "探索之间流畅切换的智能体奠定了基础。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 影响声明 =====
add_heading("影响声明", level=1)
add_para("本文所呈现的工作旨在推动机器学习领域的发展。我们的工作存在许多潜在的社会影响，但我们认为没有哪一项需要在此特别强调。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 参考文献 =====
add_heading("参考文献", level=1)
add_para("（注：参考文献按学术惯例保留原文，不进行翻译。）", size=9, space_after=6,
         color=RGBColor(0x66,0x66,0x66))

# ===== 附录 =====
doc.add_page_break()
add_heading("附录 A  附录", level=1)

add_heading("A.1  实验细节", level=2)
add_para("模型：CoT 与潜思维链（Coconut）模型都基于最小尺寸的 GPT-2 变体，具有 124M 参数。对潜思维链，我们在所有实验中使用 M = 6 "
         "个潜推理步。潜在思维向量 h_k 与 GPT-2 的隐藏大小具有相同维度（d = 768）。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("训练：我们使用 Adam 优化器，学习率 1e−4，权重衰减 0.01。训练在 4 块 GPU 上进行，采用混合精度（ProsQA 启用 bfloat16，"
         "GSM8K 因稳定性考虑禁用）。对 GSM8K，训练 25 个 epoch，batch 大小 32，梯度累积步数 1；对 ProsQA，训练 30 个 epoch，"
         "batch 大小 16，梯度累积步数 2。Coconut 课程逐阶段推进：对 GSM8K，在每个阶段使用 3 个 epoch，直到潜阶段 3（即把前 3 个 "
         "CoT 步压缩为潜思维）；对 ProsQA，在每个阶段使用 4 个 epoch，直到潜阶段 6（全内化）。基础模型检查点从标准 GPT-2 初始化。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("数据集：我们在两个推理基准上评估：", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_para("1. GSM8K：我们使用标准划分，留出包含 330 个样本的测试集。训练与验证分别使用官方训练集（7,473 个样本）与 10% 验证子集。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=3, indent=18)
add_para("2. ProsQA：遵循 Hao et al.（2024b），我们使用包含 300 个样本的测试集。训练与验证集分别包含 2,000 与 200 个样本。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, indent=18)
add_para("所有报告的准确率都在这些测试集上计算。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("符号指数可视化细节：图1 与图2 中的可视化基于各自测试集中有代表性的样本。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("• 图1（GSM8K）：该图由以下数学推理问题生成：“Janet 的鸭子每天下 16 个蛋。她每天早上吃 3 个当早餐，每天用 4 个给朋友烤松饼。"
        "她每天以每个 2 美元的价格把剩余的蛋在农贸市场卖掉。她每天在农贸市场能赚多少美元？”",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, indent=18)
add_para("• 图2（ProsQA）：该图由以下逻辑推理问题生成：涉及一系列“每个 X 是 Y”的类型包含关系（shumpus、yumpus、worpus 等），"
        "并提问“Fae 是 gwompus 还是 bompus？”（完整命题列表见英文原文）。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, indent=18)
add_para("噪声注入协议：推理期间，我们按如下方式注入高斯噪声 N(0, σ²I_d)：", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_para("1. 对 CoT：噪声加到 LM 头之前的最后一个隐藏状态，即 h ← h + σ·ϵ，其中 ϵ ~ N(0, I_d)。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=3, indent=18)
add_para("2. 对潜思维链：在每个推理步加入噪声，即 h_k ← f_θ(h_{k−1}) + σ·ϵ_k，使用独立的 ϵ_k ~ N(0, I_d)。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, indent=18)
add_para("我们报告准确率作为测试集上的精确匹配率。图3 中的「准确率下降比」定义为 Acc(σ)/Acc(0)。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("可复现性：所有实验使用种子 0。由于我们评测协议的确定性性质，以及对符号指数估计使用固定的 p = 0.95 的核采样（nucleus sampling），"
         "给定相同的模型检查点，结果完全可复现。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

add_heading("A.2  定理4.1 的证明", level=2)
add_para("引理 A.1（损失与互信息）：假设解码器模型族 {p_θ(S^(k+1…M) | h_k, X)} 是良设定的，即存在参数 θ* 使 "
         "p_θ*(S^(k+1…M) | h_k, X) = p(S^(k+1…M) | h_k, X) 几乎处处成立。进一步假设 H(S^(k+1…M) | X) < ∞。则",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_para("min_θ L_CoT^(k)(θ) ⇔ max_{p(h_k|X)} I(h_k; S^(k+1…M) | X)。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_para("证明：展开损失函数：" + "\n" +
         "L_CoT^(k)(θ) = E_{p(X,S,h_k)}[−log p_θ(S^(k+1…M) | h_k, X)]" + "\n" +
         "= E_{p(X,h_k)}[ E_{p(S^(k+1…M)|X,h_k)}[−log p_θ(S^(k+1…M) | h_k, X)] ]" + "\n" +
         "= E_{p(X,h_k)}[ H(S^(k+1…M) | h_k, X) + D_KL(p(·|h_k,X) ‖ p_θ(·|h_k,X)) ]。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_para("由良设定假设，存在 w* 使 D_KL(p(·|h_k,X) ‖ p_θ(·|h_k,X)) → 0。因此，min_θ L_CoT^(k)(θ) = min_{p(h_k|X)} H(S^(k+1…M) | h_k, X)。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("（定理4.1 的证明参见附录，此处保留其信息论推导。核心结论：Coconut 在第 k 阶段的目标等价于条件信息瓶颈问题，"
         "其最优编码器位于信息平面的效率前沿，且 β(k) ~ k/(M − k)。）", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("A.3  定理4.3 的证明", level=2)
add_para("引理 A.2（CoT 输出分布熵 H(p_CoT) 的上界）：令 p̄ = E[p_CoT] 为 B 个选项上的期望后继分布，来自具有参数 α 与集中度 "
         "κ = Σ_i α_i 的狄利克雷先验。在高集中——即对某个 j，α_j ≫ α_{i≠j}——的情况下，熵 H(p̄) 随 κ 增大而消失。"
         "具体地，若 α_j = κ − (B−1)c 且 α_{i≠j} = c（c 为小的正常数），则 H(p̄) = O(log κ / κ)。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("（定理4.3 的证明：通过狄利克雷分布的强大数定律，当 κ → ∞ 时 p_CoT 几乎必然收敛到其均值；再由 KL 散度作为概率向量连续函数"
         "的性质，可得 D_KL(q_PR ‖ p_CoT) = ((B−1)/B)·log κ − log B − ((B−1)/B)·log c + O(1/κ)。由于 H(p_CoT) → 0，且 D_KL 随 κ 对数增长，"
         "这证明了 CoT 的探索不足。）", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("A.4  定理4.5 的证明", level=2)
add_para("假设 A.3（潜在状态的收敛与紧致性）：我们假设推理期间，潜在状态序列 {h_k} 随推理步 k 增大而收敛到不动点或进入紧致吸引集。"
         "这不仅是一个理论便利，也是我们在实证中一致观察到的行为。如图5 所示，潜在思维嵌入的 PCA 可视化揭示了清晰的收敛轨迹，"
         "其中连续状态 {L1, …, L6} 在有界区域内逐渐靠拢。前两个主成分的高解释方差（0.99）确认了这一二维投影忠实刻画了原始高维空间"
         "中的动力学。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_image(os.path.join(FIG, "fig05.png"), width_in=6.3)
add_caption("图5：推理轨迹的潜在状态嵌入的 PCA 可视化。在 (a) 与 (b) 中，潜在思维（L1–L6）都表现出清晰的收敛，支持关于潜在状态"
            "存在紧致吸引集的假设。这验证了收敛动力学是潜在推理过程的一般性质，而非特定于单一任务。", size=9)
add_para("引理 A.4（Coconut 的非退化输出分布）：对于通过 Coconut 目标训练的模型，其优化可以建模为求解具有有限权衡参数 β(k) > 0 的"
         "条件信息瓶颈（CIB）问题（定理4.1）。在此框架下，模型的输出概率分布是非退化的：存在常数 δ > 0，使得对任意有效后继词元 u "
         "与任意可达潜在状态 h，概率严格有界于 1：", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_math(os.path.join(MATH, "eq_A4.png"), width_in=4.4)
add_para("其中 H 是由假设 A.3 保证的紧致潜在状态空间。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("（定理4.5 的证明：由引理 A.4，存在 δ > 0 使 max_u p(u|h) ≤ 1 − δ。求取最大化 D_KL 的最集中分布（在约束下），可得上界 "
         "D_KL(q_PR ‖ p_Coconut) ≤ −((B−1)/B)·log δ − c ≤ −(1/2)·log δ − c，与分支因子 B 无关。这确保了潜思维链维持非退化分布，"
         "与 CoT 的无界散度形成对比。）", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

add_heading("A.5  定理4.7 的证明", level=2)
add_para("证明：我们通过对推理步 k 归纳，证明在次决策扰动下，显式 CoT 轨迹 Ŝ 与无噪声轨迹 S* 相同。令 f_θ(·) 表示模型的确定性前向传播。"
         "在第 k 步，模型取输入 x 与离散历史 S^(1…k−1)，产生逻辑向量 l*_k = f_θ(x, S^(1…k−1))。无噪声词元选择为 s*_k = argmax(l*_k)。"
         "扰动过程产生逻辑值 l̂_k = l*_k + ϵ_k，其中 ϵ_k 满足次决策条件：argmax(l*_k + ϵ_k) = argmax(l*_k)。由归纳假设 ŝ_k = s*_k "
         "对所有 k = 1, …, M 成立，因此轨迹发散的概率为 0，即 P[Ŝ ≠ S*] = 0。这数学上确认了第4.3节所述的离散化重置机制："
         "argmax 算子充当非线性滤波器，在每一步把内部状态重置为干净的整数网格，防止次决策噪声累积。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

add_heading("A.6  定理4.8 的证明", level=2)
add_para("证明：从递推 E_k = f_θ(h_{k−1}) − f_θ(h*_{k−1}) + ϵ_h^(k)，取平方范数与期望，并利用噪声的独立性与零均值性质（使交叉项消失），"
         "我们得到递推 E[‖E_k‖²] ≤ L_F²·E[‖E_{k−1}‖²] + d·σ²_h。结合初始条件 E[‖E_0‖²] = 0 求解这一非齐次线性递推，得到："
         "当 L_F ≠ 1 时 E[‖E_M‖²] = ((1 − L_F^{2M})/(1 − L_F²))·d·σ²_h；当 L_F = 1 时 E[‖E_M‖²] = M·d·σ²_h。"
         "两种情况都对任意 M ≥ 1 有 E[‖E_M‖²] > 0，证毕。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("（这一非线性项说明期望平方误差随 M 增长；若转移函数扩张（L_F > 1）则误差复合，即使稳定（L_F ≤ 1）也仍累积，"
         "解释了潜思维链在 GSM8K 等精度敏感任务上的退化。）", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("A.7  归一化准确率函数的推导", level=2)
add_para("本节给出归一化准确率曲线 A(σ) 的严格推导，以解释图3 中观察到的特征性逆 S 形（类 sigmoid）退化。我们把「潜在空间注入噪声」到"
         "「输出空间词元排序的概率性失败」建模为因果链。先对隐藏状态中的噪声累积建模（与定理4.8 一致），得到一个由累积噪声向量 "
         "ϵ_acc ~ N(0, σ²_eff I_d) 扰动的最终状态 h̃_M。投影到逻辑空间后，成功条件等价于 ξ < Δl，其中 ξ = η_{j*} − η_{i*}，"
         "Δl 即逻辑决策裕度。由于 ξ 是各向同性高斯的线性组合，ξ ~ N(0, σ²_1)，且 σ_1 = √C·σ。于是归一化准确率：",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
add_math(os.path.join(MATH, "eq_Acc.png"), width_in=3.4)
add_para("（式4）", size=9)
add_para("这一推导为实验结果提供了严谨的物理解释。在 σ → 0 的极限下，参数 Δl/(√C·σ) → ∞，A(σ) → 1。这解释了「次决策平台」，其中"
         "准确率保持稳定，因为噪声严格限于安全裕度 Δl 之内。随着 σ 增大，参数减小，导致准确率曲线上特征性的类 sigmoid 衰减。"
         "这确认了鲁棒性由符号指数诱导的裕度 Δl 与累积噪声方差之比解析地决定。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)

add_heading("A.8  定理4.11 的证明", level=2)
add_para("证明：逻辑决策裕度 Δl 定义为首、次最可能词元逻辑值之差，Δl = l*_i − l*_j。我们旨在基于符号指数 I_S 建立这一量的下界。"
         "先用 softmax 函数把逻辑值联系到概率，p_i = e^{l_i} / Σ_k e^{l_k}，则前两个词元概率之比为 p_{i*}/p_{j*} = e^{Δl}。"
         "取自然对数得 Δl = log(p_{i*}) − log(p_{j*})。由符号指数定义，p_{i*} = I_S。对 p_{j*}，因所有概率之和为 1，"
         "除最可能词元外的概率之和为 1 − I_S，故 p_{j*} ≤ 1 − I_S。对数单调递增，故 −log(p_{j*}) ≥ −log(1 − I_S)。"
         "代入得 Δl = log(I_S) − log(p_{j*}) ≥ log(I_S / (1 − I_S))，即所证下界。", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

add_heading("A.9  定理4.12 的证明", level=2)
add_para("证明：理想均匀先验 q_PR（q_i = 1/B，i = 1, …, B）与模型输出分布 p 之间的 KL 散度为 D_KL(q_PR‖p) = −log B − (1/B)·Σ_i log p_i。"
         "为找到 D_KL 的下界，需在模型分布的约束（Σ p_i = 1 与 max_i p_i = I_S）下求 Σ_i log p_i 的上界。"
         "令 p_{i*} = I_S，其余 B − 1 个概率之和为 1 − I_S。函数 Σ_{k≠i*} log p_k 是凹的，由 Jensen 不等式，当其余概率尽可能均匀，"
         "即 p_k = (1 − I_S)/(B − 1)（k ≠ i*）时该和最大。代入得 Σ_i log p_i = log(I_S) + (B − 1)·log((1 − I_S)/(B − 1))。"
         "回代到 KL 表达式，其下界为 D_KL(q_PR‖p) ≥ −log B − (1/B)·[log(I_S) + (B − 1)·log((1 − I_S)/(B − 1))]，证毕。",
         size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

add_heading("A.10  定理5.1 的证明", level=2)
add_para("证明：我们通过构造反例证明。定义一个推理任务，其偏置训练分布的成功率严格低于专家，并证明最大似然估计（MLE）收敛到模仿"
         "这种次优行为的策略，导致永久性性能差距。（构造要点：考虑 d = 3 的潜在空间，三个离散状态 h_expert（特征 [1,0,0]ᵀ）、"
         "h_shortcut（[0,1,1]ᵀ）与 h_bad（[0,1,0]ᵀ）；估值函数 V(h) 在 h = h_expert 时为 1，否则为 0。专家参数 θ* = [10,0,0]ᵀ，"
         "成功率约 1.0。而偏置数据分布把全部质量放在 h_shortcut 上，故 R(P_biased) = 0，满足条件 R(P_biased) ≤ R(θ*) − Δ（Δ ≈ 1）。"
         "在偏置数据上做 MLE 会驱动 θ_2 + θ_3 → ∞，所得策略把概率质量整体移至捷径，最终 R(θ̂_MLE) ≈ 0。故 R(θ̂_MLE) ≤ R(θ*) − C "
         "（C ≈ 1）。这证明没有课程纠正分布偏置时，模型性能永久有界地偏离最优。）", size=10.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

add_heading("A.11  定理5.2 的证明", level=2)
add_para("对模仿学习框架的论证：我们的理论分析，特别是定理5.2，把训练过程建模在标准模仿学习（IL）框架内。该框架假设可访问从专家潜在策略 "
         "P_θ*(h|x) 采样的输入—潜在状态对的独立同分布数据集。通过信息论推导（见英文原文完整证明），Coconut 训练虽然形式上监督于"
         "未来词元生成，但其内在的 CIB 目标迫使编码器生成的潜在状态分布 p_θ(h|x) 拟合隐式专家潜在策略 P_θ*(h|x)。因此，在专家轨迹"
         "数据集上最小化 Coconut 损失，数学上等价于在由 h*_i = E_θ*(S*_{i,past}) 构造的隐式数据集上做 MLE，从而为把基于 IL 的理论保证"
         "应用于 Coconut 模型提供了严谨基础。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("引理 A.5（向量鞅的自归一化界，Abbasi-yadkori et al., 2011）与引理 A.6（参数估计置信集的构造）：在标准正则条件下"
         "（有界特征、强凸性、次高斯得分、有界参数），可构造非渐近、高概率的置信集，其半径 β_n(δ) = C·(d log(n) + log(1/δ))/n，"
         "以概率 ≥ 1 − δ 覆盖真实专家参数 θ*。", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
add_para("（定理5.2 的证明：由引理 A.6 可把 KL 散度界化为界；再用 Pinsker 不等式把 KL 界转为总变差（TV）距离界；"
         "最后利用有界函数下 TV 距离支配期望差的性质，得到 |SuccessRate(θ̂) − SuccessRate(θ*)| ≤ O(√((d log n + log(1/δ))/n))。"
         "故成功率以高概率收敛到专家，速率 O(√((d log n)/n))，证毕。）", size=10.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)

# ===== 保存 =====
OUT_PATH = os.path.join(OUT_DIR, "潜思维链的能力与根本局限_中文翻译.docx")
doc.save(OUT_PATH)
print("SAVED:", OUT_PATH)
