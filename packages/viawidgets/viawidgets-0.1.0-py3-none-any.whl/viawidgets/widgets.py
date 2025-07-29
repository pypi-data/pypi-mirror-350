import pathlib
import pandas as pd
import numpy as np
from traitlets import List, Integer, Unicode

from .base import ViaWidget


class CounterWidget(ViaWidget):
    _esm = """
    function render({ model, el }) {
      let count = () => model.get("value");
      let btn = document.createElement("button");
      btn.classList.add("counter-button");
      btn.innerHTML = `count is ${count()}`;
      btn.addEventListener("click", () => {
        model.set("value", count() + 1);
        model.save_changes();
      });
      model.on("change:value", () => {
        btn.innerHTML = `count is ${count()}`;
      });
      el.appendChild(btn);
    }
    export default { render };
    """
    _css = """
    .counter-button {
      background-image: linear-gradient(to right, #a1c4fd, #c2e9fb);
      border: 0;
      border-radius: 10px;
      padding: 10px 50px;
      color: white;
    }
    """
    value = Integer(0).tag(sync=True)


class ClusteringLinkConstraintsWidget(ViaWidget):
    _esm = pathlib.Path(__file__).parent / "JS" / "ClusteringLinkConstraintsWidget.js"
    _css = pathlib.Path(__file__).parent / "CSS" / "ClusteringLinkConstraintsWidget.css"
    df_indices = List(Integer(), default_value=[]).tag(sync=True)
    must_link_constraints = List(List(Integer()), default_value=[]).tag(sync=True)
    cannot_link_constraints = List(List(Integer()), default_value=[]).tag(sync=True)
    text_labels = List(Unicode(), default_value=[]).tag(sync=True)

    def __init__(
        self,
        df: pd.DataFrame,
        clustering_result_columns,
        n=10,
        text_label_column=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.df = df
        self.clustering_result_columns = clustering_result_columns
        self.df_indices = [
            int(idx) for idx in np.random.choice(df.index, size=n, replace=False)
        ]
        if text_label_column and text_label_column in df.columns:
            self.text_labels = list(df.loc[self.df_indices, text_label_column])

    def get_eligible_cr(self):
        result_columns = self.clustering_result_columns
        filtered_df = self.df.loc[self.df_indices][result_columns]

        for must_link_constraint in self.must_link_constraints:
            columns_with_same_value = (
                filtered_df.loc[must_link_constraint].nunique() == 1
            )
            result_columns = columns_with_same_value[
                columns_with_same_value
            ].index.tolist()
            if len(result_columns) == 0:
                return result_columns
            filtered_df = filtered_df[result_columns]

        for cannot_link_constraint in self.cannot_link_constraints:
            columns_with_different_value = (
                filtered_df.loc[cannot_link_constraint].nunique() == 2
            )
            result_columns = columns_with_different_value[
                columns_with_different_value
            ].index.tolist()
            if len(result_columns) == 0:
                return result_columns
            filtered_df = filtered_df[result_columns]

        return result_columns
