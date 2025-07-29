from xer_parser.model.classes.task import Task
from xer_parser.model.classes.taskactv import TaskActv
from xer_parser.model.classes.taskpred import TaskPred

__all__ = ["Tasks"]


class Tasks:
    """
    This class is a collection of tasks that controls functionalities to search, add, update and delete tasks
    """

    def __init__(self) -> None:
        self.index = 0
        self._tasks = []

    def add(self, params, data) -> None:
        task = Task(params, data)
        self._tasks.append(task)

    @property
    def activities(self) -> list[Task]:
        return self._tasks

    @property
    def count(self) -> int:
        return len(self._tasks)

    @property
    def has_no_successor(self) -> list:
        return list(
            filter(
                lambda x: x.task_id not in [z.pred_task_id for z in TaskPred.obj_list],
                self._tasks,
            )
        )

    @property
    def has_no_predecessor(self) -> list:
        return list(
            filter(
                lambda x: x.task_id not in [z.task_id for z in TaskPred.obj_list],
                self._tasks,
            )
        )

    def __len__(self) -> int:
        return len(self._tasks)

    def __repr__(self) -> str:
        return str([x.task_code for x in self._tasks])

    def __str__(self) -> str:
        return str([str(x.task_code) for x in self._tasks])

    @property
    def constraints(self) -> list:
        lst = [
            x.constraints if x.constraints is not None else None for x in self._tasks
        ]
        # print(lst)
        return list(filter(lambda x: x is not None, lst))

    def find_by_id(self, id):  # TODO: Add correct return type annotation
        obj = list(filter(lambda x: x.task_id == id, self._tasks))
        if len(obj) > 0:
            return obj[0]
        return obj

    def find_by_code(self, code):  # TODO: Add correct return type annotation
        obj = list(filter(lambda x: x.task_code == code, self._tasks))
        if len(obj) > 0:
            return obj[0]
        return obj

    def duration_greater_than(
        self, duration
    ):  # TODO: Add correct return type annotation
        obj = list(
            filter(
                lambda x: x.target_drtn_hr_cnt
                > duration * float(self.calendar.day_hr_cnt),
                self._tasks,
            )
        )
        if obj:
            return obj
        return obj

    def float_less_than(self, Tfloat):  # TODO: Add correct return type annotation
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        obj = list(
            filter(
                lambda x: x.total_float_hr_cnt < Tfloat * float(x.calendar.day_hr_cnt),
                objs,
            )
        )
        if obj:
            return obj
        return obj

    def float_greater_than(self, Tfloat):  # TODO: Add correct return type annotation
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        obj = list(
            filter(
                lambda x: x.total_float_hr_cnt > Tfloat * float(x.calendar.day_hr_cnt),
                objs,
            )
        )
        if obj:
            return obj
        return obj

    def float_within_range(self, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        if float1 < float2:
            obj = list(
                filter(
                    lambda x: x.total_float_hr_cnt
                    >= float1 * float(x.calendar.day_hr_cnt)
                    and x.total_float_hr_cnt <= float2 * float(x.calendar.day_hr_cnt),
                    objs,
                )
            )
            if obj:
                return obj
        return obj

    def float_within_range_exclusive(self, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        if float1 < float2:
            obj = list(
                filter(
                    lambda x: x.total_float_hr_cnt
                    > float1 * float(x.calendar.day_hr_cnt)
                    and x.total_float_hr_cnt < float2 * float(x.calendar.day_hr_cnt),
                    objs,
                )
            )
            if obj:
                return obj
        return obj

    def activities_by_status(self, status):
        return list(filter(lambda x: x.status_code == status, self._tasks))

    def activities_by_wbs_id(self, id):
        return list(filter(lambda x: x.wbs_id == id, self._tasks))

    def activities_by_activity_code_id(self, id):
        objs = list(filter(lambda x: x.actv_code_id == id, TaskActv.obj_list))
        activities = []
        for obj in objs:
            activities.append(self.find_by_id(obj.task_id))
        return activities

    def no_predecessors(self):
        return list(
            filter(
                lambda x: x.task_id not in [z.task_id for z in TaskPred.obj_list],
                self._tasks,
            )
        )

    def no_successors(self):
        return list(
            filter(
                lambda x: x.task_id not in [z.pred_task_id for z in TaskPred.obj_list],
                self._tasks,
            )
        )

    def activities_with_hard_contratints(self):
        return list(
            filter(
                lambda x: x.cstr_type == "CS_MEO" or x.cstr_type == "CS_MSO",
                self._tasks,
            )
        )

    def activities_by_type(self, type):
        return list(filter(lambda x: x.cstr_type == type, self._tasks))

    def get_tsv(self):
        tsv = []
        if len(self._tasks) > 0:
            tsv.append(["%T", "TASK"])
            tsv.append(
                [
                    "%F",
                    "task_id",
                    "proj_id",
                    "wbs_id",
                    "clndr_id",
                    "phys_complete_pct",
                    "rev_fdbk_flag",
                    "est_wt",
                    "lock_plan_flag",
                    "auto_compute_act_flag",
                    "complete_pct_type",
                    "task_type",
                    "duration_type",
                    "status_code",
                    "task_code",
                    "task_name",
                    "rsrc_id",
                    "total_float_hr_cnt",
                    "free_float_hr_cnt",
                    "remain_drtn_hr_cnt",
                    "act_work_qty",
                    "remain_work_qty",
                    "target_work_qty",
                    "target_drtn_hr_cnt",
                    "target_equip_qty",
                    "act_equip_qty",
                    "remain_equip_qty",
                    "cstr_date",
                    "act_start_date",
                    "act_end_date",
                    "late_start_date",
                    "late_end_date",
                    "expect_end_date",
                    "early_start_date",
                    "early_end_date",
                    "restart_date",
                    "reend_date",
                    "target_start_date",
                    "target_end_date",
                    "rem_late_start_date",
                    "rem_late_end_date",
                    "cstr_type",
                    "priority_type",
                    "suspend_date",
                    "resume_date",
                    "float_path",
                    "float_path_order",
                    "guid",
                    "tmpl_guid",
                    "cstr_date2",
                    "cstr_type2",
                    "driving_path_flag",
                    "act_this_per_work_qty",
                    "act_this_per_equip_qty",
                    "external_early_start_date",
                    "external_late_end_date",
                    "create_date",
                    "update_date",
                    "create_user",
                    "update_user",
                    "location_id",
                ]
            )
            for task in self._tasks:
                tsv.append(task.get_tsv())
        return tsv

    def get_by_project(self, id):
        return list(filter(lambda x: x.proj_id == id, self._tasks))

    def __iter__(self) -> "Tasks":
        return self

    def __next__(self) -> Task:
        if self.index >= len(self._tasks):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._tasks[idx]
