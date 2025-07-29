import logging
from typing import Any, ClassVar, Optional

from xer_parser.model.classes.task import Task

# Initialize logger
logger = logging.getLogger(__name__)


class WBS:
    """
    Represents a Work Breakdown Structure (WBS) element in Primavera P6.

    This class encapsulates the WBS elements that organize activities hierarchically
    within a project structure. WBS provides a framework for organizing and defining
    the total scope of the project.

    Parameters
    ----------
    params : Dict[str, Any]
        Dictionary of parameters from the XER file
    data : Any, optional
        Reference to the main data container

    Attributes
    ----------
    wbs_id : int
        Unique identifier for the WBS element
    proj_id : int
        Project ID to which this WBS belongs
    wbs_name : str
        Name of the WBS element
    wbs_short_name : str
        Short name of the WBS element
    parent_wbs_id : int
        ID of the parent WBS element in the hierarchy
    status_code : str
        Status code of the WBS element
    """

    obj_list: ClassVar[list["WBS"]] = []

    def __init__(self, params: dict[str, Any], data: Any = None) -> None:
        """
        Initialize a WBS object from XER file parameters.

        Parameters
        ----------
        params : Dict[str, Any]
            Dictionary of parameters from the XER file
        data : Any, optional
            Reference to the main data container
        """
        self.wbs_id = (
            int(params.get("wbs_id").strip()) if params.get("wbs_id") else None
        )
        self.proj_id = (
            int(params.get("proj_id").strip()) if params.get("proj_id") else None
        )
        self.obs_id = params.get("obs_id").strip()
        self.seq_num = params.get("seq_num").strip()
        self.est_wt = params.get("est_wt")
        self.proj_node_flag = params.get("proj_node_flag").strip()
        self.sum_data_flag = params.get("sum_data_flag").strip()
        self.status_code = params.get("status_code").strip()
        self.wbs_short_name = params.get("wbs_short_name").strip()
        self.wbs_name = params.get("wbs_name").strip()
        self.phase_id = params.get("phase_id").strip()
        self.parent_wbs_id = (
            int(params.get("parent_wbs_id")) if params.get("parent_wbs_id") else None
        )
        self.ev_user_pct = params.get("ev_user_pct").strip()
        self.ev_etc_user_value = params.get("ev_etc_user_value").strip()
        self.orig_cost = params.get("orig_cost").strip()
        self.indep_remain_total_cost = params.get("indep_remain_total_cost").strip()
        self.ann_dscnt_rate_pct = params.get("ann_dscnt_rate_pct").strip()
        self.dscnt_period_type = params.get("dscnt_period_type").strip()
        self.indep_remain_work_qty = params.get("indep_remain_work_qty").strip()
        self.anticip_start_date = params.get("anticip_start_date").strip()
        self.anticip_end_date = params.get("anticip_end_date").strip()
        self.ev_compute_type = params.get("ev_compute_type").strip()
        self.ev_etc_compute_type = params.get("ev_etc_compute_type").strip()
        self.guid = params.get("guid").strip()
        self.tmpl_guid = params.get("tmpl_guid").strip()
        self.plan_open_state = (
            params.get("plan_open_state").strip()
            if params.get("plan_open_state")
            else None
        )
        self.data = data
        WBS.obj_list.append(self)

    def get_id(self) -> int:
        """
        Get the WBS ID.

        Returns
        -------
        int
            The unique identifier for this WBS element
        """
        return self.wbs_id

    def get_tsv(self) -> list[Any]:
        return [
            "%R",
            self.wbs_id,
            self.proj_id,
            self.obs_id,
            self.seq_num,
            self.est_wt,
            self.proj_node_flag,
            self.sum_data_flag,
            self.status_code,
            self.wbs_short_name,
            self.wbs_name,
            self.phase_id,
            self.parent_wbs_id,
            self.ev_user_pct,
            self.ev_etc_user_value,
            self.orig_cost,
            self.indep_remain_total_cost,
            self.ann_dscnt_rate_pct,
            self.dscnt_period_type,
            self.indep_remain_work_qty,
            self.anticip_start_date,
            self.anticip_end_date,
            self.ev_compute_type,
            self.ev_etc_compute_type,
            self.guid,
            self.tmpl_guid,
            self.plan_open_state,
        ]

    @classmethod
    def get_json(cls) -> dict[str, Any]:
        root_nodes = list(
            filter(lambda x: WBS.find_by_id(x.parent_wbs_id) is None, cls.obj_list)
        )
        logger.info(root_nodes)
        json = {}
        for node in root_nodes:
            json["node"] = node
            json["level"] = 0
            json["childs"] = []
            json["childs"].append(cls.get_childs(node, 0))
        logger.info(json)
        return json

    @classmethod
    def get_childs(cls, node: "WBS", level: int) -> dict[str, Any]:
        nodes_lst = list(filter(lambda x: x.parent_wbs_id == node.wbs_id, cls.obj_list))
        nod = {}
        for node in nodes_lst:
            nod["node"] = node
            nod["level"] = level + 1
            children = cls.get_childs(node, level + 1)
            nod["childs"] = []
            nod["childs"].append(children)
        return nod

    @classmethod
    def find_by_id(cls, id_: int | None) -> Optional["WBS"]:
        obj = list(filter(lambda x: x.wbs_id == id_, cls.obj_list))
        if obj:
            return obj[0]
        return None

    @classmethod
    def find_by_project_id(cls, project_id: int) -> list["WBS"]:
        """
        Find all WBS elements belonging to a project.

        Parameters
        ----------
        project_id : int
            The project ID to search for

        Returns
        -------
        List[WBS]
            List of WBS elements belonging to the specified project
        """
        return [v for v in cls.obj_list if v.proj_id == project_id]

    @property
    def activities(self) -> list[Task]:
        """
        Get all activities associated with this WBS element.

        Returns
        -------
        List[Task]
            List of tasks belonging to this WBS element
        """
        return self.data.tasks.activities_by_wbs_id(self.wbs_id)

    def __repr__(self) -> str:
        """
        String representation of the WBS element.

        Returns
        -------
        str
            The WBS element's name
        """
        return self.wbs_name
