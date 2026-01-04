class VisualizationService:
    @staticmethod
    def generate_visualization(data: dict, viz_type: str, config: dict = None) -> dict:
        """生成可视化数据
        
        Args:
            data: 要可视化的数据
            viz_type: 可视化类型，支持：
                - radar: 雷达图
                - bar: 柱状图
                - line: 折线图
                - pie: 饼图
                - heatmap: 热力图
                - network: 网络图
                - table: 表格
            config: 可视化配置参数
            
        Returns:
            dict: 可视化数据
        """
        if not config:
            config = {}
        
        # 根据可视化类型生成对应的数据
        if viz_type == "radar":
            viz_data = VisualizationService._generate_radar_chart(data, config)
        elif viz_type == "bar":
            viz_data = VisualizationService._generate_bar_chart(data, config)
        elif viz_type == "line":
            viz_data = VisualizationService._generate_line_chart(data, config)
        elif viz_type == "pie":
            viz_data = VisualizationService._generate_pie_chart(data, config)
        elif viz_type == "heatmap":
            viz_data = VisualizationService._generate_heatmap(data, config)
        elif viz_type == "network":
            viz_data = VisualizationService._generate_network_chart(data, config)
        elif viz_type == "table":
            viz_data = VisualizationService._generate_table(data, config)
        else:
            raise ValueError(f"Unsupported visualization type: {viz_type}")
        
        return {
            "status": "success",
            "visualization": {
                "type": viz_type,
                "data": viz_data,
                "config": config
            }
        }
    
    @staticmethod
    def _generate_radar_chart(data: dict, config: dict) -> dict:
        """生成雷达图数据
        
        Args:
            data: 要可视化的数据
            config: 可视化配置参数
            
        Returns:
            dict: 雷达图数据
        """
        # 数据格式示例：
        # {
        #     "categories": ["技术优势", "业务优势", "管理优势", "综合优势"],
        #     "series": [
        #         {
        #             "name": "主持人",
        #             "values": [0.8, 0.6, 0.7, 0.9]
        #         },
        #         {
        #             "name": "嘉宾",
        #             "values": [0.9, 0.7, 0.6, 0.8]
        #         }
        #     ]
        # }
        
        # 确保数据格式正确
        if "categories" not in data:
            data["categories"] = config.get("categories", [])
        
        if "series" not in data:
            # 从values自动生成series
            if "values" in data:
                data["series"] = [{
                    "name": config.get("series_name", "数据"),
                    "values": data["values"]
                }]
            else:
                data["series"] = []
        
        return {
            "categories": data["categories"],
            "series": data["series"],
            "options": {
                "title": config.get("title", "雷达图"),
                "subtitle": config.get("subtitle", ""),
                "showLegend": config.get("showLegend", True),
                "showTooltip": config.get("showTooltip", True),
                "colorScheme": config.get("colorScheme", ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"])
            }
        }
    
    @staticmethod
    def _generate_bar_chart(data: dict, config: dict) -> dict:
        """生成柱状图数据
        
        Args:
            data: 要可视化的数据
            config: 可视化配置参数
            
        Returns:
            dict: 柱状图数据
        """
        # 数据格式示例：
        # {
        #     "categories": ["概念1", "概念2", "概念3"],
        #     "series": [
        #         {
        #             "name": "主持人",
        #             "values": [10, 20, 30]
        #         },
        #         {
        #             "name": "嘉宾",
        #             "values": [15, 25, 35]
        #         }
        #     ]
        # }
        
        # 确保数据格式正确
        if "categories" not in data:
            data["categories"] = config.get("categories", [])
        
        if "series" not in data:
            # 从values自动生成series
            if "values" in data:
                data["series"] = [{
                    "name": config.get("series_name", "数据"),
                    "values": data["values"]
                }]
            else:
                data["series"] = []
        
        return {
            "categories": data["categories"],
            "series": data["series"],
            "options": {
                "title": config.get("title", "柱状图"),
                "subtitle": config.get("subtitle", ""),
                "showLegend": config.get("showLegend", True),
                "showTooltip": config.get("showTooltip", True),
                "colorScheme": config.get("colorScheme", ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]),
                "orientation": config.get("orientation", "vertical"),  # vertical or horizontal
                "showGrid": config.get("showGrid", True)
            }
        }
    
    @staticmethod
    def _generate_line_chart(data: dict, config: dict) -> dict:
        """生成折线图数据
        
        Args:
            data: 要可视化的数据
            config: 可视化配置参数
            
        Returns:
            dict: 折线图数据
        """
        # 数据格式示例：
        # {
        #     "categories": ["时间1", "时间2", "时间3"],
        #     "series": [
        #         {
        #             "name": "指标1",
        #             "values": [10, 20, 30]
        #         },
        #         {
        #             "name": "指标2",
        #             "values": [15, 25, 35]
        #         }
        #     ]
        # }
        
        # 确保数据格式正确
        if "categories" not in data:
            data["categories"] = config.get("categories", [])
        
        if "series" not in data:
            # 从values自动生成series
            if "values" in data:
                data["series"] = [{
                    "name": config.get("series_name", "数据"),
                    "values": data["values"]
                }]
            else:
                data["series"] = []
        
        return {
            "categories": data["categories"],
            "series": data["series"],
            "options": {
                "title": config.get("title", "折线图"),
                "subtitle": config.get("subtitle", ""),
                "showLegend": config.get("showLegend", True),
                "showTooltip": config.get("showTooltip", True),
                "colorScheme": config.get("colorScheme", ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]),
                "showGrid": config.get("showGrid", True),
                "smooth": config.get("smooth", False),
                "showPoints": config.get("showPoints", True)
            }
        }
    
    @staticmethod
    def _generate_pie_chart(data: dict, config: dict) -> dict:
        """生成饼图数据
        
        Args:
            data: 要可视化的数据
            config: 可视化配置参数
            
        Returns:
            dict: 饼图数据
        """
        # 数据格式示例：
        # {
        #     "series": [
        #         {
        #             "name": "概念1",
        #             "value": 30
        #         },
        #         {
        #             "name": "概念2",
        #             "value": 20
        #         },
        #         {
        #             "name": "概念3",
        #             "value": 50
        #         }
        #     ]
        # }
        
        # 确保数据格式正确
        if "series" not in data:
            # 从labels和values自动生成series
            if "labels" in data and "values" in data:
                data["series"] = []
                for label, value in zip(data["labels"], data["values"]):
                    data["series"].append({
                        "name": label,
                        "value": value
                    })
            else:
                data["series"] = []
        
        return {
            "series": data["series"],
            "options": {
                "title": config.get("title", "饼图"),
                "subtitle": config.get("subtitle", ""),
                "showLegend": config.get("showLegend", True),
                "showTooltip": config.get("showTooltip", True),
                "colorScheme": config.get("colorScheme", ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]),
                "showLabels": config.get("showLabels", True),
                "showPercentages": config.get("showPercentages", True)
            }
        }
    
    @staticmethod
    def _generate_heatmap(data: dict, config: dict) -> dict:
        """生成热力图数据
        
        Args:
            data: 要可视化的数据
            config: 可视化配置参数
            
        Returns:
            dict: 热力图数据
        """
        # 数据格式示例：
        # {
        #     "xAxis": ["概念1", "概念2", "概念3"],
        #     "yAxis": ["主持人", "嘉宾"],
        #     "values": [
        #         [0.8, 0.6, 0.7],
        #         [0.9, 0.7, 0.6]
        #     ]
        # }
        
        # 确保数据格式正确
        if "xAxis" not in data:
            data["xAxis"] = config.get("xAxis", [])
        
        if "yAxis" not in data:
            data["yAxis"] = config.get("yAxis", [])
        
        if "values" not in data:
            data["values"] = config.get("values", [])
        
        return {
            "xAxis": data["xAxis"],
            "yAxis": data["yAxis"],
            "values": data["values"],
            "options": {
                "title": config.get("title", "热力图"),
                "subtitle": config.get("subtitle", ""),
                "showLegend": config.get("showLegend", True),
                "showTooltip": config.get("showTooltip", True),
                "colorScheme": config.get("colorScheme", "viridis"),  # 热力图支持内置颜色方案
                "showLabels": config.get("showLabels", True),
                "labelFormat": config.get("labelFormat", "{value:.2f}")
            }
        }
    
    @staticmethod
    def _generate_network_chart(data: dict, config: dict) -> dict:
        """生成网络图数据
        
        Args:
            data: 要可视化的数据
            config: 可视化配置参数
            
        Returns:
            dict: 网络图数据
        """
        # 数据格式示例：
        # {
        #     "nodes": [
        #         {
        #             "id": "node1",
        #             "label": "主持人",
        #             "type": "person",
        #             "size": 10
        #         },
        #         {
        #             "id": "node2",
        #             "label": "嘉宾",
        #             "type": "person",
        #             "size": 8
        #         },
        #         {
        #             "id": "node3",
        #             "label": "技术",
        #             "type": "concept",
        #             "size": 6
        #         }
        #     ],
        #     "edges": [
        #         {
        #             "source": "node1",
        #             "target": "node3",
        #             "type": "提及",
        #             "strength": 0.8
        #         },
        #         {
        #             "source": "node2",
        #             "target": "node3",
        #             "type": "提及",
        #             "strength": 0.6
        #         }
        #     ]
        # }
        
        # 确保数据格式正确
        if "nodes" not in data:
            data["nodes"] = []
        
        if "edges" not in data:
            data["edges"] = []
        
        return {
            "nodes": data["nodes"],
            "edges": data["edges"],
            "options": {
                "title": config.get("title", "网络图"),
                "subtitle": config.get("subtitle", ""),
                "layout": config.get("layout", "force-directed"),  # force-directed, circular, hierarchical
                "showLegend": config.get("showLegend", True),
                "showTooltip": config.get("showTooltip", True),
                "nodeColorScheme": config.get("nodeColorScheme", "#3498db"),
                "edgeColorScheme": config.get("edgeColorScheme", "#95a5a6"),
                "nodeSizeField": config.get("nodeSizeField", "size"),
                "edgeWidthField": config.get("edgeWidthField", "strength")
            }
        }
    
    @staticmethod
    def _generate_table(data: dict, config: dict) -> dict:
        """生成表格数据
        
        Args:
            data: 要可视化的数据
            config: 可视化配置参数
            
        Returns:
            dict: 表格数据
        """
        # 数据格式示例：
        # {
        #     "columns": [
        #         {"id": "name", "label": "名称", "type": "string"},
        #         {"id": "value", "label": "值", "type": "number"},
        #         {"id": "description", "label": "描述", "type": "string"}
        #     ],
        #     "rows": [
        #         {"name": "概念1", "value": 10, "description": "这是概念1"},
        #         {"name": "概念2", "value": 20, "description": "这是概念2"},
        #         {"name": "概念3", "value": 30, "description": "这是概念3"}
        #     ]
        # }
        
        # 确保数据格式正确
        if "columns" not in data:
            # 自动生成列定义
            if "rows" in data and data["rows"]:
                first_row = data["rows"][0]
                data["columns"] = []
                for key, value in first_row.items():
                    # 自动检测类型
                    col_type = "string"
                    if isinstance(value, (int, float)):
                        col_type = "number"
                    elif isinstance(value, bool):
                        col_type = "boolean"
                    data["columns"].append({
                        "id": key,
                        "label": key.capitalize(),
                        "type": col_type
                    })
            else:
                data["columns"] = []
        
        if "rows" not in data:
            data["rows"] = []
        
        return {
            "columns": data["columns"],
            "rows": data["rows"],
            "options": {
                "title": config.get("title", "表格"),
                "subtitle": config.get("subtitle", ""),
                "showHeader": config.get("showHeader", True),
                "showPagination": config.get("showPagination", True),
                "pageSize": config.get("pageSize", 10),
                "sortable": config.get("sortable", True),
                "filterable": config.get("filterable", True),
                "exportable": config.get("exportable", True)
            }
        }
    
    @staticmethod
    def generate_dashboard(dashboard_config: dict) -> dict:
        """生成仪表盘数据
        
        Args:
            dashboard_config: 仪表盘配置，包含多个可视化组件
            
        Returns:
            dict: 仪表盘数据
        """
        components = []
        
        # 生成每个可视化组件
        for component in dashboard_config.get("components", []):
            viz_data = VisualizationService.generate_visualization(
                component["data"],
                component["type"],
                component.get("config", {})
            )
            
            components.append({
                "id": component["id"],
                "type": component["type"],
                "title": component.get("title", ""),
                "subtitle": component.get("subtitle", ""),
                "position": component.get("position", {"x": 0, "y": 0, "width": 4, "height": 3}),
                "visualization": viz_data["visualization"]
            })
        
        return {
            "status": "success",
            "dashboard": {
                "title": dashboard_config.get("title", "仪表盘"),
                "subtitle": dashboard_config.get("subtitle", ""),
                "components": components,
                "layout": dashboard_config.get("layout", "grid"),  # grid, free
                "theme": dashboard_config.get("theme", "light")  # light, dark
            }
        }
