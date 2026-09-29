# `perspmat` 到底是什么

## —— `source/blender/editors/space_view3d/view3d_project.cc:120~151` 深度数学解析

> 配套文件：`perspmat与投影数学深挖.html`（同内容的 HTML 版，含深度精度曲线图）

---

## 0. 一句话回答

`perspmat` **不是** GL 状态机里那个单独的 `GL_PROJECTION` 矩阵，而是

$$\texttt{persmat} = \texttt{winmat} \cdot \texttt{viewmat} = P \cdot V$$

也就是图形学里常说的 **VP 矩阵（View-Projection）**：一次矩阵乘法直接把**世界空间**坐标送到**裁剪空间**。

所谓"**已合成**"，是指本该在 GPU 顶点着色器里分两步完成的

```glsl
vec4 clip = P * (V * vec4(pos, 1.0));
```

被提前乘成一步 `(P·V) * vec4(pos, 1.0)`，并把结果缓存在 `rv3d->persmat` 里。

- **代价**：每次视口重绘算一次 4×4 矩阵乘法（`view3d_draw.cc:135`）
- **收益**：每次投影少一次 4×4 矩阵乘法 —— 而投影处在极热的循环里（选中拾取、边迭代器、gizmo 绘制，每帧对每个顶点调用）

---

## 1. 证据链：`persmat` 的来源

### 1.1 合成点（每次重绘只做一次）

```c
/* view3d_draw.cc:135 */
mul_m4_m4m4(rv3d->persmat, rv3d->winmat, rv3d->viewmat);
invert_m4_m4(rv3d->persinv, rv3d->persmat);
invert_m4_m4(rv3d->viewinv, rv3d->viewmat);
```

```c
/* space_view3d.cc:132 —— 再乘上物体矩阵，供物体空间投影使用 */
mul_m4_m4m4(rv3d->viewmatob, rv3d->viewmat, ob->object_to_world().ptr());
mul_m4_m4m4(rv3d->persmatob, rv3d->persmat, ob->object_to_world().ptr());
```

### 1.2 DNA 里的权威注释

`makesdna/DNA_view3d_types.h:467-482` 对这几个字段的注释写得非常明确：

| 字段 | DNA 注释 | 实际含义 |
|---|---|---|
| `rv3d->winmat` | `GL_PROJECTION matrix.` | 只负责 **视图空间 → 裁剪空间**。与相机位置无关，只由 FOV / 正交缩放 / 近远裁剪面决定 |
| `rv3d->viewmat` | `GL_MODELVIEW matrix.` | 只负责 **世界空间 → 视图空间**。是相机变换的逆，刚体矩阵（正交且行列式 $+1$） |
| `rv3d->persmat` | `Viewmat*winmat.` | $= \texttt{winmat} \cdot \texttt{viewmat}$，直接从世界空间到裁剪空间，等价于 GLSL 里的 `P * V` |
| `rv3d->persinv` | `Inverse of persmat.` | 逆向：裁剪空间 → 世界空间（射线拾取用） |
| `rv3d->persmatob` | `viewmat/persmat multiplied with object matrix` | $= \texttt{persmat} \cdot M_{obj}$，等价于 `P * V * M`，直接从物体局部空间到裁剪空间 |

### 1.3 完整变换链

```
co（世界空间 / 物体空间）
  │
  ├─ viewmat（刚体变换，相机变换的逆）
  ▼
视图空间 (x_view, y_view, z_view)
  │
  ├─ winmat（GL_PROJECTION：frustum 或 ortho）
  ▼
裁剪空间 (x_c, y_c, z_c, w)
  │
  ├─ 除以 w（透视除法 / perspective divide）
  ▼
NDC ∈ [-1, 1]³
  │
  ├─ fx = winx/2 · (1 + x_ndc)
  ▼
窗口像素坐标 (fx, fy)
```

在代码里，前三步被折叠成 **第 122 行的唯一一次** `mul_m4_v4(perspmat, vec4)`。

---

## 2. 为什么"合成"在数学上完全免费

### 2.1 结合律

矩阵乘法满足结合律：

$$(P \cdot V) \cdot v \;=\; P \cdot (V \cdot v)$$

先把 `viewmat` 和 `winmat` 乘起来存好，跟每次投影时连乘两次，**结果逐位相同**（浮点误差量级也基本一致）。差别只在**计算次数**：前者是每次重绘 1 次矩阵乘法，后者是每次投影 2 次矩阵-向量乘法。所以预合成是纯粹的**性能优化**，不改变任何语义。

### 2.2 Blender 的存储约定：`m[列][行]`，列主序

`float mat[4][4]` 在内存里是 16 个连续 float，**`mat[i]` 是第 $i$ 列**。这样可以直接喂给 `glUniformMatrix4fv(..., GL_FALSE, ...)` 而不用转置。所以：

$$\texttt{mat[c][r]} = M_{r,c}, \qquad \texttt{mat[3][0..2]} = \text{平移分量}$$

**读 Blender 矩阵代码时，下标顺序和数学教科书是反的，这是第一个高频踩坑点。**

### 2.3 乘法约定：`mul_m4_m4m4(R, A, B)` 计算 $R = A \cdot B$

`math_matrix_c.cc:226` 的注释 `R[j][k] = B[j][i] . A[i][k]` 用的正是 `[列][行]` 下标。展开验证第 0 项（`math_matrix_c.cc:245`）：

```c
R[0][0] = B[0][0]*A[0][0] + B[0][1]*A[1][0] + B[0][2]*A[2][0] + B[0][3]*A[3][0];
```

换成标准数学下标（把 `X[c][r]` 记作 $X_{r,c}$）：

$$R_{0,0} = B_{0,0}A_{0,0} + B_{1,0}A_{0,1} + B_{2,0}A_{0,2} + B_{3,0}A_{0,3} = \sum_k A_{0,k}B_{k,0} = (A \cdot B)_{0,0}$$

所以 **`mul_m4_m4m4(R, A, B)` 得到 $R = A \cdot B$，语义是"先作用 A，再作用 B"**（对列向量左乘而言）。这就对上了：

- `mul_m4_m4m4(persmat, winmat, viewmat)` → $persmat = P \cdot V$ → 先 viewmat 后 winmat，即**世界 → 视图 → 裁剪**，顺序正确。
- `mul_m4_m4m4(persmatob, persmat, object_to_world)` → $P \cdot V \cdot M$，物体空间先经过 $M$。

### 2.4 原地乘法的别名安全性

`mul_m4_v4(mat, r)` 内部是 `mul_v4_m4v4(r, mat, r)`（`math_matrix_c.cc:812`），**输入输出是同一块内存**。看实现（`math_matrix_c.cc:798-808`）：

```c
void mul_v4_m4v4(float r[4], const float mat[4][4], const float v[4])
{
  const float x = v[0];   /* 先读进局部变量 */
  const float y = v[1];
  const float z = v[2];

  r[0] = x * mat[0][0] + y * mat[1][0] + z * mat[2][0] + mat[3][0] * v[3];
  r[1] = x * mat[0][1] + y * mat[1][1] + z * mat[2][1] + mat[3][1] * v[3];
  r[2] = x * mat[0][2] + y * mat[1][2] + z * mat[2][2] + mat[3][2] * v[3];
  r[3] = x * mat[0][3] + y * mat[1][3] + z * mat[2][3] + mat[3][3] * v[3];
}
```

先把 `v[0..2]` 读进局部变量，写 `r[0..2]` 时不再依赖原值，**最后才读 `v[3]`** —— 所以别名是安全的。第 122 行正依赖这一点。

---

## 3. 齐次坐标与射影几何

这是理解 120–135 行**全部数学**的地基。

### 3.1 仿射点的齐次嵌入

三维仿射空间 $\mathbb{A}^3$ 中的点 $(x,y,z)$ 嵌入射影空间 $\mathbb{P}^3$ 时写成 $(x,y,z,1)$。这就是 120–121 行在干的事：

```c
copy_v3_v3(vec4, co);
vec4[3] = 1.0;
```

补上那个 $1$，是为了让 $4\times4$ 矩阵能**同时表达线性变换和平移** —— 纯线性变换只能表达过原点的变换；平移在 $\mathbb{A}^3$ 里是仿射而非线性映射，但在 $\mathbb{P}^3$ 里它就是一个货真价实的线性映射。

### 3.2 射影等价与透视除法

$\mathbb{P}^3$ 的元素是**等价类**：任何非零 $\lambda$ 缩放的四个数代表同一个射影点

$$(x,y,z,w) \;\sim\; (\lambda x, \lambda y, \lambda z, \lambda w), \qquad \lambda \neq 0$$

为了回到唯一的仿射坐标，约定"归一化到 $w=1$"，于是**必须除以 $w$**：

$$(x_c, y_c, z_c, w) \;\longmapsto\; \left(\frac{x_c}{w},\ \frac{y_c}{w},\ \frac{z_c}{w},\ 1\right)$$

**这就是"透视除法"（perspective divide）的全部来历** —— 它不是图形学发明的技巧，而是射影几何的定义直接推出来的。第 138–139 行的 `* scalar`（$= 1/w$）干的就是这件事。

### 3.3 $w=0$ 是无穷远点

$w=0$ 的射影点是**无穷远点**：无论 $\lambda$ 怎么缩放，都无法把 $w$ 变成 $1$，因此无法映射回仿射空间。这解释了：

- 第 125 行 `CLIP_ZERO` 的存在 —— 必须显式拦截这类点；
- 第 137 行那个兜底 `(w != 0.0f) ? (1.0f / w) : 0.0f` —— 防止产生 `inf` / `NaN` 污染后续计算。

---

## 4. 针孔相机模型：为什么 $w = -z_{view}$

### 4.1 相似三角形

真实相机成像的基本关系是**相似三角形**：物体离得越远，成像越小，缩放因子恰为 $1/\text{深度}$。

$$x_{ndc} \propto \frac{x_{view}}{-z_{view}}, \qquad y_{ndc} \propto \frac{y_{view}}{-z_{view}}$$

负号是因为 Blender / OpenGL 约定相机朝 $-z$ 方向看，所以相机**前方**的点满足 $z_{view} < 0$，于是 $-z_{view} > 0$ 才是正的深度。

要让后续的"除以 $w$"自动实现这个 $1/\text{深度}$，就必须让 $w$ 正比于深度。

### 4.2 frustum 矩阵展开

看 `gpu/intern/gpu_matrix.cc:309-333` 的 `mat4_frustum_set`：

```c
m[0][0] = 2.0f * near / (right - left);
m[1][1] = 2.0f * near / (top - bottom);
m[2][2] = -(far + near) / (far - near);
m[3][2] = -2.0f * far * near / (far - near);
m[2][3] = -1.0f;   /* 存储下标 [列][行] = 数学上的第 3 行第 2 列 */
```

展开成标准数学矩阵（记 $n$ = 近裁剪面，$f$ = 远裁剪面，$l,r,b,t$ 为视锥四边界）：

$$P = \begin{bmatrix}
\dfrac{2n}{r-l} & 0 & \dfrac{r+l}{r-l} & 0 \\[8pt]
0 & \dfrac{2n}{t-b} & \dfrac{t+b}{t-b} & 0 \\[8pt]
0 & 0 & -\dfrac{f+n}{f-n} & -\dfrac{2fn}{f-n} \\[8pt]
0 & 0 & -1 & 0
\end{bmatrix}$$

用 `mul_v4_m4v4` 的公式算第 4 个分量：

$$w = x\cdot 0 + y\cdot 0 + z\cdot(-1) + 1\cdot 0 = -z_{view}$$

**精确成立。** 所以"除以 $w$"就等价于"除以深度"，透视缩放自动实现。

> **第 4 行 $(0,0,-1,0)$ 就是整个透视投影的灵魂** —— 它是唯一让 $w \neq 1$ 的一行。

### 4.3 正交矩阵对比

`gpu_matrix.cc:283-304` 的 `mat4_ortho_set`，第 4 行是 $(0,0,0,1)$，所以：

$$w \equiv 1$$

除法变成恒等操作，没有透视缩放 —— 这正是正交投影的定义。

---

## 5. 120–122 行的逐步数值演示

取 $n = 0.1$、$f = 1000$，视锥上下左右对称（$l=-r$、$b=-t$），于是 $\frac{r+l}{r-l} = 0$、$\frac{t+b}{t-b} = 0$，矩阵简化为对角形式。

取世界空间中相机正前方 10 个单位处、且 $x_{view} = y_{view} = 0$ 的点，则 $z_{view} = -10$：

```
第 1 步  copy_v3_v3(vec4, co);      →  vec4 = [0, 0, -10, ?]
第 2 步  vec4[3] = 1.0;             →  vec4 = [0, 0, -10, 1]     ← 齐次嵌入
第 3 步  mul_m4_v4(perspmat, vec4);

         x_c = 2n/(r-l) · 0                         = 0
         y_c = 2n/(t-b) · 0                         = 0
         z_c = -(f+n)/(f-n) · (-10) + (-2fn/(f-n)) · 1
             = (1000.1/999.9) · 10 − 200/999.9
             = 10.0010 − 0.2000                     = 9.8010
         w   = -1 · (-10)                           = 10      ← w = -z_view
```

得到裁剪空间坐标 $(0,\ 0,\ 9.801,\ 10)$，且 $\frac{z_c}{w} = 0.9801$，落在 $[-1,1]$ 内，可见。

---

## 6. 第 123 行：`fabsf` 到底改了什么

```c
const float w = fabsf(vec4[3]);
```

**`w` 从此不再是"齐次坐标的第 4 分量"，而变成了"该点到相机平面的距离"（以视图空间单位为量纲）。** 三个后果：

1. **第 137 行 `scalar = 1/w` 恒为正**，所以 $x_c/|w|$ 与真正的射影值 $x_c/\texttt{vec4[3]}$ 相差一个符号 —— 相机背后的点会被投影到**镜像位置**，而不是被拒绝。
2. **`CLIP_ZERO` 的语义被改写**：从"$w$ 为负或为零"变成"**到相机平面的距离 ≤ 0.001**"。否则所有相机背后的点都会被误报成 `CLIP_ZERO`。
3. **真正负责拦截背后点的是 `CLIP_NEAR`**（第 129 行），推导见下一节。

对比文件开头 32–51 行的"**不裁剪版**"：

```c
if (vec4[3] > FLT_EPSILON) {          /* 只对前方点做除法 */
  co_region[0] = region->winx / 2.0f + (region->winx / 2.0f) * vec4[0] / vec4[3];
  co_region[1] = region->winy / 2.0f + (region->winy / 2.0f) * vec4[1] / vec4[3];
}
else {
  zero_v2(co_region);                 /* 背后点 → (0,0)，没有状态码 */
}
```

它用的是**原始** `vec4[3]`（保留符号），代价是**无法区分"背后"和"恰好在相机平面上"**，也没有任何状态码返回。裁剪版（本段）改用 $|w|$ 加独立的状态码，把"背后"这件事显式交给 `CLIP_NEAR` 处理 —— 这是一次**职责的重新划分**，不是随手取了个绝对值。

---

## 7. 125–135 行：不做除法的"交叉相乘"比较

这三行是整段代码最精巧的地方。它们的**数学本质**是把有理不等式 $\frac{z_c}{w} \lessgtr \pm 1$ 两边同乘 $w$，变成有界浮点乘法。

### 7.1 `CLIP_NEAR` 推导（第 129 行）

```c
if ((flag & V3D_PROJ_TEST_CLIP_NEAR) && (vec4[2] <= -w)) {
  return V3D_PROJ_RET_CLIP_NEAR;
}
```

GL 的裁剪空间约定是 $\frac{z_c}{w} \in [-1, 1]$，其中 **$-1$ 对应近平面**。两边同乘 $w > 0$：

$$\frac{z_c}{w} \le -1 \quad\Longleftrightarrow\quad z_c \le -w$$

### 7.2 近/远平面映射验算

**近平面** $z_{view} = -n$：

$$z_c = -\frac{f+n}{f-n}\cdot(-n) - \frac{2fn}{f-n} = \frac{n(f+n) - 2fn}{f-n} = \frac{n^2 - nf}{f-n} = -n$$

而 $w = -z_{view} = n$，所以 $\dfrac{z_c}{w} = \dfrac{-n}{n} = -1$ ✓

**远平面** $z_{view} = -f$：

$$z_c = -\frac{f+n}{f-n}\cdot(-f) - \frac{2fn}{f-n} = \frac{f(f+n) - 2fn}{f-n} = \frac{f^2 - fn}{f-n} = f$$

而 $w = f$，所以 $\dfrac{z_c}{w} = \dfrac{f}{f} = +1$ ✓

### 7.3 `CLIP_FAR` 推导（第 133 行）

```c
if ((flag & V3D_PROJ_TEST_CLIP_FAR) && (vec4[2] >= w)) {
  return V3D_PROJ_RET_CLIP_FAR;
}
```

同一套推导，$\dfrac{z_c}{w} \ge +1 \Longleftrightarrow z_c \ge w$。

### 7.4 为什么必须"先判后除"

1. **省一次除法**：浮点除法延迟通常是乘法的 4–20 倍，在每帧数万次的顶点循环里很可观。
2. **数值稳健**：$w$ 极小时 $\frac{z_c}{w}$ 会溢出成 `inf`，或产生灾难性抵消（catastrophic cancellation）；而 $z_c$ 与 $w$ 的比较始终是良态的有界比较。**除法被推迟到所有可能出问题的点都已经被过滤之后** —— 这正是第 137 行排在 125–135 行之后的原因。
3. **数学等价**：两个不等式合起来恰好是 $|z_c| > w$ 的两个半边，与 $\left|\frac{z_c}{w}\right| > 1$ 完全等价。

### 7.5 数值表（$n=0.1$, $f=1000$）

| $z_{view}$ | $w = \lvert\vec4[3]\rvert$ | $z_c$ | $z_c / w$ | 触发 | 返回状态 |
|---:|---:|---:|---:|---|---|
| -0.05 | 0.05 | -0.15 | -3.00 | NEAR | `CLIP_NEAR` |
| -1 | 1 | 0.800 | 0.800 | — | `OK` |
| -10 | 10 | 9.801 | 0.980 | — | `OK` |
| -1000 | 1000 | 1000.0 | 1.000 | FAR | `CLIP_FAR` |
| -2000 | 2000 | 2000.2 | 1.000 | FAR | `CLIP_FAR` |
| **+5（相机背后）** | 5 | -5.201 | -1.040 | **NEAR** | **`CLIP_NEAR`** |

注意最后一行：$z_{view} = +5$ 时 $\vec4[3] = -5$，取绝对值后 $w = 5$，NEAR 判据 $-5.201 \le -5$ 成立 → 返回 `CLIP_NEAR`。

**相机背后的点是靠 NEAR 兜住的**：因为 $z_c$ 随 $z_{view}$ 增大而急剧变负，必然跌破 $-w$。这也正是 `ED_view3d.hh:313-316` 要求"透视视图必须把 `CLIP_WIN` 和 `CLIP_NEAR` 一起打开"的原因。

### 7.6 深度精度分布

把 $z_{view} = -d$（$d > 0$ 为深度）代入，得到 NDC 深度关于深度的解析式：

$$\text{ndc}(d) = \frac{z_c}{w} = \frac{(f+n)\,d - 2fn}{(f-n)\,d} \quad\xrightarrow{\ n=0.1,\ f=1000\ }\quad \frac{1000.1\,d - 200}{999.9\,d}$$

| 深度 $d$ | 0.1 | 0.15 | 0.2 | 0.3 | 0.5 | 1 | 2 | 5 | 10 | 20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ndc | -1.000 | -0.333 | 0.000 | 0.334 | 0.600 | 0.800 | 0.900 | 0.960 | 0.980 | 0.990 |

这张表揭示了一个经典现象：**深度精度严重非均匀**。

- $d \in [0.1,\ 1]$ 这一小段就用掉了 NDC 的 **40%**（$-1 \to 0.80$）
- $d \in [1,\ 10]$ 用掉约 **18%**
- $d \in [10,\ 1000]$ 全部挤在最后 **2%** 里

$d \to 0^+$ 时曲线冲向 $-\infty$，这就是 `CLIP_ZERO` 存在的理由。这也是所有透视深度缓冲（z-fighting）问题的数学根源。

---

## 8. 正交投影下的退化

正交矩阵 $w \equiv 1$，于是：

- **`CLIP_NEAR`**：$z_c \le -1$；**`CLIP_FAR`**：$z_c \ge 1$ —— 判据依旧精确（7.2 节已验算近远平面分别映射到 $\mp 1$）。
- **`CLIP_ZERO` 永远不会触发**（$1 > 0.001$）：没有除法，也就不存在 $w \to 0$ 的奇点。
- **"相机背后"在正交下不再是奇点**：正交投影是仿射映射，$z_{view} > 0$ 的点只会因为落在 $[-n, -f]$ 这个**立方体视景体**之外而被 NEAR 裁掉 —— 这与透视下"投影奇点"是完全不同的物理原因。

---

## 9. 一个容易踩的坑：`CLIP_CONTENT` 不在这里

`V3D_PROJ_TEST_ALL` 包含 `V3D_PROJ_TEST_CLIP_CONTENT`（所以第 109 行的断言能通过），但 **120–135 行从不检查这一位**。

它由 `view3d_iterators.cc` 的边迭代器消费，语义是"把跨越视口边界的边裁剪到边界上"（见 `ED_view3d.hh:301-321`），与单点投影无关。

> **所以读这三行时不要去找 `CLIP_CONTENT` 的分支 —— 它确实不在。**

---

## 10. 总结

| 行号 | 做什么 | 数学本质 |
|---|---|---|
| 120–121 | `copy_v3_v3` + `vec4[3] = 1.0` | 仿射点的**齐次嵌入** $\mathbb{A}^3 \hookrightarrow \mathbb{P}^3$ |
| 122 | `mul_m4_v4(perspmat, vec4)` | 一步完成 $P \cdot V \cdot v$（**预合成的 VP 矩阵**） |
| 123 | `w = fabsf(vec4[3])` | 把"齐次第 4 分量"改写成"到相机平面的**距离**"，代价是丢失符号 |
| 125–127 | `CLIP_ZERO` | $w \to 0$ 即射影**无穷远点**，无法回到仿射空间 |
| 129–131 | `CLIP_NEAR` | $\frac{z_c}{w} \le -1 \Leftrightarrow z_c \le -w$，**交叉相乘免除法**；同时兜住相机背后的点 |
| 133–135 | `CLIP_FAR` | $\frac{z_c}{w} \ge +1 \Leftrightarrow z_c \ge w$，同一套推导 |

**一句话**：`perspmat` 是 $P \cdot V$（世界 → 裁剪的完整线性映射），"已合成"就是把本该在 GPU 顶点着色器里分两步做的 `P * (V * pos)` 预先乘成一步；而 120–135 行则是**射影几何的直接翻译** —— 补 $1$ 做齐次嵌入 → 一次矩阵乘法进裁剪空间 → 用 $z_c$ 与 $w$ 交叉相乘代替除以 $w$ 来做深度裁剪 → 最后才真正除以 $w$ 落到 NDC。

---

## 附：关键源码位置索引

| 内容 | 文件:行 |
|---|---|
| `persmat` 合成 | `source/blender/editors/space_view3d/view3d_draw.cc:135` |
| `persmatob` 合成 | `source/blender/editors/space_view3d/space_view3d.cc:132` |
| DNA 字段注释 | `source/blender/makesdna/DNA_view3d_types.h:467-482` |
| frustum 矩阵 | `source/blender/gpu/intern/gpu_matrix.cc:309-333` |
| ortho 矩阵 | `source/blender/gpu/intern/gpu_matrix.cc:283-304` |
| `mul_m4_m4m4` 实现 | `source/blender/blenlib/intern/math_matrix_c.cc:217-263` |
| `mul_v4_m4v4` 实现 | `source/blender/blenlib/intern/math_matrix_c.cc:798-808` |
| 不裁剪版投影 | `source/blender/editors/space_view3d/view3d_project.cc:32-74` |
| 裁剪版投影 | `source/blender/editors/space_view3d/view3d_project.cc:99-151` |
| 状态码 / 测试位定义 | `source/blender/editors/include/ED_view3d.hh:271-333` |
| BB 裁剪实现 | `source/blender/editors/space_view3d/view3d_draw.cc:2252-2265` |
