# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Simple visualization of quantum circuits. These codes refer to
https://github.com/microsoft/quantum-viz.js/
"""

from collections import defaultdict
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib import patches

single_gate = [
    "H",
    "X",
    "Y",
    "Z",
    "S",
    "T",
    "SD",
    "TD",
    "X2M",
    "X2P",
    "Y2M",
    "Y2P",
    "M",
]
multi_gate = ["CZ", "CY", "CX", "CNOT"]
theta_gate = ["RX", "RY", "RZ"]


class DrawError(Exception):
    """Draw error."""


def get_continuous_gate(opt, qlist):
    qindex = {}
    for q, i in zip(qlist, range(len(qlist))):
        qindex[q] = i
    idx = []
    idx_map = {}
    for q in opt.targets:
        idx.append(qindex[q])
        idx_map[qindex[q]] = q
    idx.append(10**7)
    idx.sort()
    continuous = []
    l, r = 0, 1
    while r < len(idx):
        if idx[r] != idx[r - 1] + 1:
            continuous.append(idx[l:r])
            l = r
        r += 1

    continuous_opt = []
    for p in continuous:
        new_opt = deepcopy(opt)
        new_opt.targets = [idx_map[i] for i in p]
        continuous_opt.append(new_opt)
    return continuous_opt


class Operation:
    def __init__(self, **kwargs) -> None:
        """create operation

        kwargs:
            gate(str): quantum gate name
            targets(list): target qubit list
            isMeasurement(bool): measurement or not
            param(str): gate's parameters
            controls(list): control qubit list
            style(dict): operation style, maybe you can change color or fontsize
        """
        self.gate = kwargs.get("gate", "")
        self.targets = kwargs.get("targets", [])
        self.isMeasurement = kwargs.get("isMeasurement", False)
        self.param = kwargs.get("param", "")
        self.controls = kwargs.get("controls", [])
        self.style = kwargs.get("style", {})

        if not self.gate:
            raise DrawError("gate can not be empty")
        if not self.targets:
            raise DrawError("target qubit can not be empty")

        qubits = self.targets + self.controls
        if len(set(qubits)) != len(qubits):
            raise DrawError("qubit reuse")
        if self.isMeasurement:
            if len(self.targets) > 1:
                raise DrawError("can only measure one qubit")
            if len(self.controls) > 0:
                raise DrawError("can not use control measure")

    def __repr__(self) -> str:
        return f"Operation(gate={self.gate}, targets={self.targets}, controls={self.controls}, isMeasurement={self.isMeasurement}, param={self.param}, style={self.style})"

    def to_dict(self):
        d = {
            "gate": self.gate,
            "targets": self.targets,
        }
        if self.controls:
            d["controls"] = self.controls
        if self.isMeasurement:
            d["isMeasurement"] = True
        if self.param:
            d["param"] = self.param
        if self.style:
            d["style"] = self.style
        return d


class Circuit:
    def __init__(self, **kwargs) -> None:
        """create circuit

        kwargs:
            qubits(list): qubit list
            operations(list): operation list, element can be dict or Operation
            max_gate_num(int): circuit depth, which will cut circuit, default is 20
            style(dict): circuit style, maybe you can change color or fontsize
            show_param(bool): wheather show parameter, like Rx(0.4)
            optimized(bool): wheather reorder circuit, avoid gate crossings
            qubits_labels(dict): qubit label, default is qubit name
            show_label(bool): wheather show lables
            gate_group(list): Use a dashed box to draw out a group of gates
        """
        self.qlist = kwargs.get("qubits", [])
        if not self.qlist:
            raise "qubit list can not be empty"
        self.qmap = {}
        self.qmap_inv = {}
        for q, i in zip(self.qlist, range(len(self.qlist))):
            self.qmap[q] = i
            self.qmap_inv[i] = q

        self.max_circuit_depth = kwargs.get("max_circuit_depth", 20)
        self.style = kwargs.get("style", {})
        self.show_param = kwargs.get("show_param", False)
        self.optimized = kwargs.get("optimized", False)
        self.qubits_labels = kwargs.get("qubits_labels", {})
        self.show_label = kwargs.get("show_label", True)
        self.gate_group = kwargs.get("gate_group", [])

        for q in self.qlist:
            if q not in self.qubits_labels:
                self.qubits_labels[q] = q

        if "operations" not in kwargs:
            raise DrawError("operations can not be empty")

        self.operations = []
        for opt in kwargs["operations"]:
            if isinstance(opt, Operation):
                self.operations.append(opt)
            elif isinstance(opt, dict):
                self.operations.append(Operation(**opt))
            else:
                raise DrawError("operation type error")
        self.build_seqs()

        self.split_gate_group = []
        m = len(self.seqs) - 1
        max_t = self.max_circuit_depth * (m) + len(self.seqs[m])
        for a, b, c, d in self.gate_group:
            if a > c or b > d:
                raise DrawError(
                    "gate group position error, need top-left and bottom-right"
                )
            if a < 0 or c >= len(self.qlist):
                raise DrawError(
                    "gate group position error, exceeding the number of qubits"
                )
            d = min(d, max_t - 1)
            while b <= d:
                nb = b + self.max_circuit_depth - b % self.max_circuit_depth
                self.split_gate_group.append([a, b, c, min(d, nb - 1)])
                b = nb

    def get_path_qubits(self, qubits):
        idx = [self.qmap[q] for q in qubits]
        s, t = min(idx), max(idx)
        path_qubits = [self.qmap_inv[i] for i in range(s, t + 1)]
        return path_qubits

    def build_seqs(self):
        node_time = defaultdict(int)
        occupy_time = defaultdict(set)

        def get_time(i):
            while node_time[i] in occupy_time[i]:
                node_time[i] += 1
            return node_time[i]

        seq_time = 0
        seqs = defaultdict(dict)
        max_t = self.max_circuit_depth
        for opt in self.operations:
            qubits = opt.targets + opt.controls
            path_qubits = qubits.copy()
            if self.optimized:
                path_qubits = self.get_path_qubits(qubits)
            t = max([get_time(q) for q in path_qubits])
            if (t % max_t) not in seqs[t // max_t]:
                seqs[t // max_t][t % max_t] = []
            seqs[t // max_t][t % max_t].append(opt)
            if self.optimized:
                for q in path_qubits:
                    occupy_time[q].add(t)
            for q in qubits:
                node_time[q] = t + 1
            seq_time = max(seq_time, t)
        self.seqs = seqs

    def to_dict(self):
        d = {
            "qubits": self.qlist,
            "operations": [opt.to_dict() for opt in self.operations],
        }
        if self.max_circuit_depth:
            d["max_circuit_depth"] = self.max_circuit_depth
        if self.style:
            d["style"] = self.style
        if self.show_param:
            d["show_param"] = self.show_param
        if self.gate_group:
            d["gate_group"] = self.gate_group
        d["show_label"] = self.show_label
        d["qubits_labels"] = self.qubits_labels
        return d

    def parse_to_latex(self):
        qcircuit = defaultdict(list)

        for m in self.seqs:
            seqs = self.seqs[m]
            for idx in range(len(seqs)):
                for q in self.qlist:
                    qcircuit[q].append("& \qw")
                for opt in seqs[idx]:
                    if opt.isMeasurement:
                        qcircuit[opt.targets[0]][-1] = "& \meter"
                    else:
                        continuous_opt = get_continuous_gate(opt, self.qlist)
                        for copt in continuous_opt:
                            if copt.gate == "X" and len(copt.controls) > 0:
                                for i, q in enumerate(copt.targets):
                                    qcircuit[q][-1] = "& \\targ"
                                    if i > 0:
                                        qcircuit[q][
                                            -1
                                        ] += f"\qwx[{-1 * (self.qmap[q] - self.qmap[copt.targets[i-1]])}]"
                            else:
                                gate_name = copt.gate
                                if self.show_param and copt.param:
                                    gate_name += copt.param
                                if len(copt.targets) > 1:
                                    qcircuit[copt.targets[0]][
                                        -1
                                    ] = f"& \multigate{{{len(copt.targets) - 1}}}{{{gate_name}}}"
                                    for i in range(1, len(copt.targets)):
                                        qcircuit[copt.targets[i]][
                                            -1
                                        ] = f"& \ghost{{{gate_name}}}"
                                else:
                                    qcircuit[copt.targets[0]][
                                        -1
                                    ] = f"& \gate{{{gate_name}}}"

                        if opt.controls:
                            for q in opt.controls:
                                qcircuit[q][-1] = "& \ctrl"
                            interval = [
                                (
                                    self.qmap[o.targets[0]],
                                    self.qmap[o.targets[-1]],
                                    "T",
                                )
                                for o in continuous_opt
                            ]
                            interval += [
                                (self.qmap[q], self.qmap[q], "C") for q in opt.controls
                            ]
                            interval.sort()
                            for i, (s, t, ch) in enumerate(interval):
                                if ch == "C":
                                    if i > 0:
                                        qcircuit[self.qmap_inv[s]][
                                            -1
                                        ] += f"{{{-1*(s - interval[i-1][1])}}}"
                                    else:
                                        qcircuit[self.qmap_inv[s]][
                                            -1
                                        ] += f"{{{(interval[i+1][0] - t)}}}"
                                else:
                                    if i > 0:
                                        qcircuit[self.qmap_inv[s]][
                                            -1
                                        ] += f"\qwx[{-1*(s - interval[i-1][1])}]"
                                    else:
                                        qcircuit[self.qmap_inv[s]][
                                            -1
                                        ] += f"\qwx[{(interval[i+1][0] - t)}]"
                        else:
                            for i in range(1, len(continuous_opt)):
                                q1, q2 = (
                                    continuous_opt[i].targets[0],
                                    continuous_opt[i - 1].targets[-1],
                                )
                                s, t = self.qmap[q1], self.qmap[q2]
                                qcircuit[q1][-1] += f"\qwx[{-1*(s - t)}]"

        return qcircuit

    def get_latex(self):
        """get latex from circuit"""
        qcircuit = self.parse_to_latex()
        latex_text = r"""\documentclass[border=2px]{standalone}
\usepackage[braket, qm]{qcircuit}
\begin{document}
\Qcircuit @C=1em @R=1em {
"""
        i = 0
        n = len(qcircuit[self.qlist[0]])
        m = n + 3
        if not self.show_label:
            m = n + 1
        while i < n:
            j = min(i + self.max_circuit_depth, n)
            for q in self.qlist:
                label = f"\\nghost{{{self.qubits_labels[q]}}} & \lstick{{{self.qubits_labels[q]}}}"
                if not self.show_label:
                    label = ""
                latex_text += f'{label} {"".join(qcircuit[q][i:j])} & \qw \\\\\n'
            latex_text += f'{"".join(["&"] * m)} \\\\\n'
            i += self.max_circuit_depth

        if self.split_gate_group:
            x_offset = 2
            if self.show_label:
                x_offset += 2
            latex_text += "\\ "
            for a, b, c, d in self.split_gate_group:
                y_offset = (b // self.max_circuit_depth) * (len(self.qlist) + 1) + 1
                b, d = b % self.max_circuit_depth, d % self.max_circuit_depth
                latex_text += f"\gategroup{{{a+y_offset}}}{{{b+x_offset}}}{{{c+y_offset}}}{{{d+x_offset}}}{{.7em}}{{--}} "
        latex_text += """}
\end{document}
"""
        return latex_text


def normalize(isq_ir):
    ir_item = isq_ir.split(" ")
    qid1 = ir_item[1]
    if ir_item[0] in single_gate:
        if ir_item[0] == "M":
            return Operation(gate=ir_item[0], targets=[qid1], isMeasurement=True)
        return Operation(gate=ir_item[0], targets=[qid1])
    elif ir_item[0] in multi_gate:
        qid2 = ir_item[2]
        if ir_item[0] in ["CX", "CNOT"]:
            return Operation(gate="X", targets=[qid2], controls=[qid1])
        if ir_item[0] == "CZ":
            return Operation(gate="Z", targets=[qid2], controls=[qid1])
        if ir_item[0] == "CY":
            return Operation(gate="Y", targets=[qid2], controls=[qid1])
    elif ir_item[0] in theta_gate:
        return Operation(
            gate=ir_item[0], targets=[qid1], param=f'({",".join(ir_item[2:])})'
        )


def get_circuit(isq_ir, **kwargs):
    """get circuit from isq ir

    Args:
        isq_ir (str): isq ir

    Returns: Circuit
    """
    isq_ir = isq_ir.strip()
    qubits = set()
    operations = []
    for ir in isq_ir.split("\n"):
        ir = ir.strip()
        if ir == "":
            continue
        opt = normalize(ir)
        operations.append(opt)
        for q in opt.targets:
            qubits.add(q)
        for q in opt.controls:
            qubits.add(q)
    qlist = list(qubits)
    qlist.sort()
    return Circuit(qubits=qlist, operations=operations, **kwargs)


class Drawer:
    def __init__(self) -> None:
        self.box_length = 1.0
        self.box_width = 1.0
        self.pad = 0.3
        self.ctrl_rad = 0.1
        self.circ_rad = 0.3
        self.xinterval = 0.3
        self.yinterval = 0.3

    def init_style(self):
        self.line_options = {"color": "black", "linewidth": 1, "zorder": 2}
        self.ctrl_line_options = {"color": "black", "linewidth": 1, "zorder": 1}
        self.group_line_options = {
            "color": "black",
            "linewidth": 1,
            "zorder": 2,
            "linestyle": (0, (10, 10)),
        }
        self.backgroud_line_options = {
            "color": "black",
            "linewidth": 1,
            "zorder": 1,
        }
        self.dash_line_options = {
            "color": "black",
            "linewidth": 1,
            "zorder": 1,
            "linestyle": "--",
        }
        self.text_options = {
            "zorder": 3,
            "ha": "center",
            "va": "center",
            "fontsize": int(self.box_width * 10),
        }
        self.box_options = {
            "facecolor": "white",
            "edgecolor": "black",
            "linewidth": 1,
            "zorder": 2,
        }
        self.arc_options = {"linewidth": 1, "zorder": 3}
        self.arrow_options = {
            "facecolor": "black",
            "edgecolor": "black",
            "linewidth": 1,
            "zorder": 3,
        }
        self.boxstyle = "square, pad=0.2"

    def set_circuit_style(self):
        for attr in self.__dict__:
            if attr.endswith("options"):
                self.__dict__[attr].update(self.circuit.style.get(attr, {}))

    def set_opt_style(self, opt):
        self.ori_box_options = deepcopy(self.box_options)
        self.ori_text_options = deepcopy(self.text_options)
        if opt.style:
            self.box_options.update(opt.style.get("box_options", {}))
            self.text_options.update(opt.style.get("text_options", {}))

    def recover_style(self):
        self.box_options = deepcopy(self.ori_box_options)
        self.text_options = deepcopy(self.ori_text_options)

    def plot(self, circuit, **kwargs):
        """plot circuit

        Args:
            circuit (str | dict | Circuit): input circuit which can be isq ir or Circuit
        """

        # change ir to circuit
        if not isinstance(circuit, Circuit):
            if isinstance(circuit, str):
                circuit = get_circuit(circuit, **kwargs)
            elif isinstance(circuit, dict):
                circuit = Circuit(**circuit)
            else:
                raise DrawError("circuit type error")

        self.show_param = circuit.show_param
        self.circuit = circuit
        self.init_style()
        self.set_circuit_style()

        self.qmap = {}
        for i, q in enumerate(self.circuit.qlist):
            self.qmap[q] = i * (self.box_length + self.yinterval)

        self.get_figure_size()
        self.set_figure()
        self.draw_circuit()
        self.draw_groups()

    def layer_height(self):
        return (
            len(self.circuit.qlist) * (self.box_length + self.yinterval)
            + self.yinterval
        )

    def get_figure_size(self):
        ax_seqs = self.circuit.seqs
        width = 0
        height = 1
        for m in ax_seqs:
            n = len(ax_seqs[m])
            ax_width = self.box_width
            for i in range(n):
                ax_width += self.get_width_of_seqs(ax_seqs[m][i])
                ax_width += self.xinterval
            ax_width -= self.xinterval
            width = max(width, ax_width)
            height += self.layer_height()
        width += 1.5
        self.figure_width = width
        self.figure_height = height

    def set_figure(self):
        self.fg = plt.figure(figsize=(self.figure_width / 2, self.figure_height / 2))
        self.ax = self.fg.add_axes(
            [0, 0, 1, 1],
            xlim=(0, self.figure_width),
            ylim=(-self.box_length, self.figure_height - 1),
            xticks=[],
            yticks=[],
        )
        self.ax.axis("off")
        self.ax.invert_yaxis()

    def draw_circuit(self):
        ax_y_offset = 0
        qnum = len(self.circuit.qlist)

        self.center = defaultdict(float)

        for m in range(len(self.circuit.seqs)):
            seqs = self.circuit.seqs[m]
            center = 1.5
            for i in range(len(seqs)):
                # get sequence center
                in_width = self.get_width_of_seqs(seqs[i])
                center += (in_width - self.box_width) / 2
                for opt in seqs[i]:
                    self.set_opt_style(opt)
                    self.add_opt(opt, center)
                    self.recover_style()
                self.center[m * self.circuit.max_circuit_depth + i] = center
                center += (in_width - self.box_width) / 2
                center += self.box_width + self.xinterval

            # plot qubit lines
            start_x = 0.5
            label_text_options = deepcopy(self.text_options)
            label_text_options["ha"] = "right"
            for i in range(qnum):
                y = i * (self.box_length + self.yinterval) + ax_y_offset
                if self.circuit.show_label:
                    self.ax.text(
                        start_x - 0.1,
                        self.qmap[self.circuit.qlist[i]],
                        f"{self.circuit.qubits_labels[self.circuit.qlist[i]]}",
                        **label_text_options,
                    )
                line = plt.Line2D(
                    (start_x, self.figure_width - 1),
                    (y, y),
                    **self.backgroud_line_options,
                )
                self.ax.add_line(line)

            ax_y_offset += self.layer_height()
            for qubit in self.qmap:
                self.qmap[qubit] += self.layer_height()

    def draw_groups(self):
        for a, b, c, d in self.circuit.split_gate_group:
            m = b // self.circuit.max_circuit_depth
            x1, x2 = self.center[b], self.center[d]
            b, d = (
                b % self.circuit.max_circuit_depth,
                d % self.circuit.max_circuit_depth,
            )
            w1 = self.get_width_of_seqs(self.circuit.seqs[m][b])
            w2 = self.get_width_of_seqs(self.circuit.seqs[m][d])
            x1 -= w1 / 2
            x2 += w2 / 2
            y1 = (
                m * self.layer_height()
                + a * (self.box_length + self.yinterval)
                - self.box_length / 2
            )
            y2 = (
                m * self.layer_height()
                + c * (self.box_length + self.yinterval)
                + self.box_length / 2
            )
            for x in [x1, x2]:
                line = plt.Line2D((x, x), (y1, y2), **self.group_line_options)
                self.ax.add_line(line)
            for y in [y1, y2]:
                line = plt.Line2D((x1, x2), (y, y), **self.group_line_options)
                self.ax.add_line(line)

    def get_width_of_seqs(self, seqs):
        width = self.box_width
        for opt in seqs:
            width = max(width, self.get_width_of_opt(opt))
        return width

    def get_width_of_opt(self, opt):
        width = self.box_width
        m = len(opt.gate)
        if self.show_param:
            m = max(m, len(opt.param))
        width = max(width, 1 * (m / 6))
        # print(opt, width)
        return width

    def box(self, x, y, box_width, box_length):
        """build a box

        Args:
            x (float): center point's x
            y (float): center point's y
            box_width (float): box width
            box_length (float): box length
        """
        pad = self.pad

        x_loc = x - box_width / 2.0 + pad
        y_loc = y - box_length / 2.0 + pad

        box = patches.FancyBboxPatch(
            (x_loc, y_loc),
            box_width - 2 * pad,
            box_length - 2 * pad,
            boxstyle=self.boxstyle,
            **self.box_options,
        )
        self.ax.add_patch(box)

    def add_ctrl_line(self, y1, y2, seq_t):
        line = plt.Line2D((seq_t, seq_t), (y1, y2), **self.ctrl_line_options)
        self.ax.add_line(line)

    def add_continuous_gate(self, opt, seq_t):
        """draw gate

        Args:
            opt (Operation): operation which need be draw
            seq_t (float): center point's x
        """

        if len(opt.controls) > 0 and opt.gate == "X":
            for i, qubit in enumerate(opt.targets):
                self.add_ctrl_x_gate(qubit, seq_t)
                if i > 0:
                    self.add_ctrl_line(
                        self.qmap[opt.targets[i - 1]], self.qmap[qubit], seq_t
                    )
        else:
            box_length = (
                self.qmap[opt.targets[-1]] - self.qmap[opt.targets[0]] + self.box_length
            )
            y = (self.qmap[opt.targets[-1]] + self.qmap[opt.targets[0]]) / 2

            box_width = self.get_width_of_opt(opt)

            self.box(seq_t, y, box_width, box_length)

            if self.show_param and opt.param != "":
                self.ax.text(
                    seq_t,
                    y + self.box_length / 8,
                    opt.param,
                    **self.text_options,
                )

                self.ax.text(
                    seq_t,
                    y - self.box_length / 8,
                    opt.gate,
                    **self.text_options,
                )
            else:
                self.ax.text(seq_t, y, opt.gate, **self.text_options)

    def add_ctrl_x_gate(self, qubit, seq_t):
        y = self.qmap[qubit]
        circ_rad = self.circ_rad
        new_options = {
            "facecolor": "white",
            "edgecolor": "black",
            "linewidth": 2,
            "zorder": 2,
        }
        target_circ = plt.Circle((seq_t, y), radius=circ_rad, **new_options)
        self.line_options["zorder"] = 3
        self.line_options["linewidth"] = 2
        target_v = plt.Line2D(
            (seq_t, seq_t), (y - circ_rad, y + circ_rad), **self.line_options
        )
        target_h = plt.Line2D(
            (seq_t - circ_rad, seq_t + circ_rad), (y, y), **self.line_options
        )
        self.line_options["zorder"] = 2
        self.line_options["linewidth"] = 1
        self.ax.add_patch(target_circ)
        self.ax.add_line(target_v)
        self.ax.add_line(target_h)

    def add_opt(self, opt, seq_t):
        if opt.isMeasurement:
            self.add_measure(opt, seq_t)
            return

        continuous_opt = get_continuous_gate(opt, self.circuit.qlist)
        for gate in continuous_opt:
            self.add_continuous_gate(gate, seq_t)
            if not opt.controls:
                for i in range(1, len(continuous_opt)):
                    q1, q2 = (
                        continuous_opt[i - 1].targets[-1],
                        continuous_opt[i].targets[0],
                    )
                    y1, y2 = self.qmap[q1], self.qmap[q2]
                    line = plt.Line2D(
                        (seq_t, seq_t), (y1, y2), **self.dash_line_options
                    )
                    self.ax.add_line(line)

        if opt.controls:
            ctrl_rad = self.ctrl_rad
            for qubit in opt.controls:
                circ_ctrl = plt.Circle(
                    (seq_t, self.qmap[qubit]),
                    radius=ctrl_rad,
                    **self.line_options,
                )
                self.ax.add_patch(circ_ctrl)

            interval = [
                (self.qmap[o.targets[0]], self.qmap[o.targets[-1]], "T")
                for o in continuous_opt
            ]
            interval += [(self.qmap[q], self.qmap[q], "C") for q in opt.controls]
            interval.sort()
            for i in range(1, len(interval)):
                y1, y2 = interval[i - 1][1], interval[i][0]
                self.add_ctrl_line(y1, y2, seq_t)

    def add_measure(self, opt, seq_t):
        """draw measure

        Args:
            opt (Operation): operation which need be draw
            seq_t (float): center point's x
        """
        y = self.qmap[opt.targets[0]]

        self.box(seq_t, y, self.box_width, self.box_length)

        box_length = self.box_length

        arc = patches.Arc(
            (seq_t, y + box_length / 5),
            0.6 * box_length,
            0.55 * box_length,
            theta1=180,
            theta2=0,
            **self.arc_options,
        )
        self.ax.add_patch(arc)

        arrow_start_x = seq_t - 0.165 * box_length
        arrow_start_y = y + 0.25 * box_length
        arrow_width = 0.35 * box_length
        arrow_height = -0.35 * box_length

        self.ax.arrow(
            arrow_start_x,
            arrow_start_y,
            arrow_width,
            arrow_height,
            head_width=box_length / 8.0,
            **self.arrow_options,
        )

    def save(self, filename):
        self.fg.savefig(f"{filename}", bbox_inches="tight")
