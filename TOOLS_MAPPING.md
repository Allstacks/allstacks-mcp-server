# Complete Allstacks API → MCP Tools Mapping

## Endpoints to Implement (Non-Admin, Non-Destructive)

### 📊 Metrics & Analytics

1. ✅ GET `/api/v1/metrics/` - List metrics
2. ✅ GET `/api/v1/metrics/{id}/` - Get metric details
3. ✅ GET `/api/v1/metrics/{id}/get_generated_metric_info/` - Get metric info
4. ✅ GET `/api/v1/project/{project_id}/generated_metric/{metric_type}` - Get generated metric
5. ✅ GET/POST `/api/v1/project/{project_id}/generated_metric_data/{metric_type}` - **MAIN GMDTS ENDPOINT**
6. ✅ POST `/api/v1/project/{project_id}/metrics_v2/metrics` - Metrics V2 data
7. ✅ POST `/api/v1/organization/{org_id}/metrics_v2/metrics` - Org Metrics V2
8. ✅ GET `/api/v1/project/{project_id}/metrics_v2/allstacks-labels/` - Get Allstacks labels
9. ✅ GET `/api/v1/project/{project_id}/metrics_v2/user-tags/` - Get user tags for metrics
10. ✅ GET `/api/v1/project/{project_id}/metrics_v2/item_props/` - Get item props for metrics
11. ✅ GET `/api/v1/project/{project_id}/insights/configs` - Insight configs
12. ✅ GET `/api/v1/project/{project_id}/metrics/` - Project metrics list
13. ✅ POST `/api/v1/organization/{org_id}/metrics_v2_capitalization/metrics` - Cap metrics V2

### 📁 Service Items

14. ✅ GET/POST `/api/v1/service_items/service_item/` - List/query service items
15. ✅ GET `/api/v1/service_items/service_item/get_property_keys/` - Get property keys by type
16. ✅ GET/POST `/api/v1/service_items/{metric}/` - Service items for metric
17. ✅ GET/POST `/api/v1/project/{project_id}/parent_service_items/` - Parent service items
18. ✅ GET `/api/v1/project/{project_id}/service_items/types/` - Service item types
19. ✅ GET `/api/v1/project/{project_id}/service_items/initial/` - Initial service items
20. ✅ GET/POST `/api/v1/project/{project_id}/service_items/estimation_method/` - Estimation methods
21. ✅ GET `/api/v1/project/{project_id}/work_bundles/types/` - Work bundle types
22. ✅ GET `/api/v1/project/{project_id}/work_bundles/initial/` - Initial work bundles
23. ✅ GET/POST `/api/v1/project/{project_id}/work_bundles/estimation_method/` - WB estimation
24. ✅ POST `/api/v1/project/{project_id}/service_item/{milestone_item_id}/notes` - Add notes
25. ✅ DELETE `/api/v1/project/{project_id}/service_item/{milestone_item_id}/notes` - Delete notes

### 🏢 Organization

26. ✅ GET `/api/v1/organization/` - List projects for organization
27. ✅ GET `/api/v1/organization/{org_id}/projects/` - Get org projects
28. ✅ GET `/api/v1/organization/{org_id}/settings/` - Organization settings
29. ✅ GET `/api/v1/organization/{org_id}/organization_settings/` - Org settings V2
30. ✅ POST `/api/v1/organization/{org_id}/organization_settings/` - Create/update org settings
31. ✅ GET `/api/v1/organization/{org_id}/company_metrics/` - Company metrics
32. ✅ POST `/api/v1/organization/{org_id}/company_metrics/` - Create company metrics
33. ✅ DELETE `/api/v1/organization/{org_id}/company_metrics/` - Delete company metrics
34. ✅ GET `/api/v1/organization/{org_id}/company_available_metrics/` - Available metrics
35. ✅ GET `/api/v1/organization/{org_id}/configuration_options/` - Configuration options
36. ✅ GET `/api/v1/organization/{org_id}/item_props/` - Item properties
37. ✅ GET `/api/v1/organization/{org_id}/item_props/{item_type}/` - Item props by type
38. ✅ GET `/api/v1/organization/{org_id}/parent_item_types/` - Parent item types
39. ✅ GET `/api/v1/organization/{org_id}/services/` - Org services
40. ✅ GET `/api/v1/organization/{org_id}/get_service_form` - Get service form
41. ✅ GET `/api/v1/organization/{org_id}/search_service` - Search services
42. ✅ GET `/api/v1/organization/{org_id}/employee_list/` - Employee list
43. ✅ GET `/api/v1/organization/{org_id}/enabled_users_count/` - Enabled users count
44. ✅ POST `/api/v1/organization/{org_id}/enable_disable_users/` - Enable/disable users
45. ✅ POST `/api/v1/organization/{org_id}/merge_users/` - Merge users
46. ✅ POST `/api/v1/organization/{org_id}/unmerge_users/` - Unmerge users

### 👥 Users & Teams

47. ✅ GET `/api/v1/organization/{org_id}/users/` - List users
48. ✅ GET `/api/v1/organization/{org_id}/users/{id}/` - Get user
49. ✅ PUT `/api/v1/organization/{org_id}/users/{id}/` - Update user
50. ✅ PATCH `/api/v1/organization/{org_id}/users/{id}/` - Partial update user
51. ✅ GET `/api/v1/organization/{org_id}/invited_users/` - List invited users
52. ✅ POST `/api/v1/organization/{org_id}/invited_users/` - Invite user
53. ✅ GET `/api/v1/organization/{org_id}/invited_users/{id}/` - Get invited user
54. ✅ PUT `/api/v1/organization/{org_id}/invited_users/{id}/` - Update invited user
55. ✅ PATCH `/api/v1/organization/{org_id}/invited_users/{id}/` - Partial update invited
56. ✅ DELETE `/api/v1/organization/{org_id}/invited_users/{id}/` - Cancel invitation
57. ✅ GET `/api/v1/organization/{org_id}/manageable_roles` - Get manageable roles
58. ✅ POST `/api/v1/organization/{org_id}/change_member_role/{member_id}/` - Change role
59. ✅ DELETE `/api/v1/organization/{org_id}/company_member/{member_id}/` - Remove member
60. ✅ POST `/api/v1/organization/{org_id}/user_without_invite/` - Create user without invite

### 🏷️ Service Users & Tags

61. ✅ GET `/api/v1/organization/{org_id}/service_user/` - List service users
62. ✅ POST `/api/v1/organization/{org_id}/service_user/get_map/` - Get user map
63. ✅ GET `/api/v1/organization/{org_id}/service_user_info/` - Service user info
64. ✅ POST `/api/v1/organization/{org_id}/service_user_info/` - Create service user info
65. ✅ DELETE `/api/v1/organization/{org_id}/service_user_info/` - Delete service user info
66. ✅ GET `/api/v1/organization/{org_id}/service_user_tag/` - List user tags
67. ✅ POST `/api/v1/organization/{org_id}/service_user_tag/` - Create tag
68. ✅ PUT `/api/v1/organization/{org_id}/service_user_tag/` - Update tag
69. ✅ DELETE `/api/v1/organization/{org_id}/service_user_tag/` - Delete tag
70. ✅ GET `/api/v1/organization/{org_id}/service_user_tag_group/` - List tag groups
71. ✅ POST `/api/v1/organization/{org_id}/service_user_tag_group/` - Create tag group
72. ✅ PUT `/api/v1/organization/{org_id}/service_user_tag_group/` - Update tag group
73. ✅ DELETE `/api/v1/organization/{org_id}/service_user_tag_group/` - Delete tag group
74. ✅ POST `/api/v1/organization/{org_id}/service_user/service_user_tags/` - Add user tags
75. ✅ PUT `/api/v1/organization/{org_id}/service_user/service_user_tags/` - Update user tags
76. ✅ DELETE `/api/v1/organization/{org_id}/service_user/service_user_tags/` - Remove user tags
77. ✅ POST `/api/v1/organization/{org_id}/service_user_tag/upload_tag_salaries` - Upload salaries
78. ✅ POST `/api/v1/organization/{org_id}/service_user_tag_hierarchy/upload_employee_tags` - Upload employee tags
79. ✅ POST `/api/v1/organization/{org_id}/service_user_tag_hierarchy/upload_tag_hierarchy` - Upload hierarchy

### 🏷️ Labels

80. ✅ GET `/api/v1/organization/{org_id}/labels/` - List labels
81. ✅ POST `/api/v1/organization/{org_id}/labels/` - Create label
82. ✅ GET `/api/v1/organization/{org_id}/labels/{id}/` - Get label
83. ✅ PUT `/api/v1/organization/{org_id}/labels/{id}/` - Update label
84. ✅ DELETE `/api/v1/organization/{org_id}/labels/{id}/` - Delete label
85. ✅ GET `/api/v1/organization/{org_id}/labels/label_families/` - List label families
86. ✅ POST `/api/v1/organization/{org_id}/labels/label_families/` - Create label family
87. ✅ PUT `/api/v1/organization/{org_id}/labels/label_families/{id}/` - Update label family
88. ✅ DELETE `/api/v1/organization/{org_id}/labels/label_families/{id}/` - Delete label family
89. ✅ POST `/api/v1/organization/{org_id}/labels/bulk_update_label_priorities/` - Bulk update priorities
90. ✅ POST `/api/v1/organization/{org_id}/labels/test/sync-all/` - Test sync labels

### 👔 Team Categories

91. ✅ GET `/api/v1/organization/{org_id}/team_categories/` - List team categories
92. ✅ POST `/api/v1/organization/{org_id}/team_categories/` - Create team category
93. ✅ PUT `/api/v1/organization/{org_id}/team_categories/{category_id}/` - Update category
94. ✅ DELETE `/api/v1/organization/{org_id}/team_categories/{category_id}/` - Delete category

### 📊 Dashboards

95. ✅ GET `/api/v1/organization/{org_id}/dashboards/` - List org dashboards
96. ✅ POST `/api/v1/organization/{org_id}/dashboards/` - Create org dashboard
97. ✅ GET `/api/v1/organization/{org_id}/dashboards/names/` - Get dashboard names
98. ✅ GET `/api/v1/organization/{org_id}/dashboards/{id}/` - Get dashboard
99. ✅ PUT `/api/v1/organization/{org_id}/dashboards/{id}/` - Update dashboard
100. ✅ PATCH `/api/v1/organization/{org_id}/dashboards/{id}/` - Partial update dashboard
101. ✅ DELETE `/api/v1/organization/{org_id}/dashboards/{id}/` - Delete dashboard
102. ✅ DELETE `/api/v1/organization/{org_id}/dashboards/{id}/clear_widgets/` - Clear widgets
103. ✅ GET `/api/v1/organization/{org_id}/dashboard_widgets/` - List widgets
104. ✅ POST `/api/v1/organization/{org_id}/dashboard_widgets/` - Create widget
105. ✅ POST `/api/v1/organization/{org_id}/dashboard_widgets/multidash/` - Create multi-dash widget
106. ✅ GET `/api/v1/organization/{org_id}/dashboard_widgets/{id}/` - Get widget
107. ✅ PUT `/api/v1/organization/{org_id}/dashboard_widgets/{id}/` - Update widget
108. ✅ PATCH `/api/v1/organization/{org_id}/dashboard_widgets/{id}/` - Partial update widget
109. ✅ DELETE `/api/v1/organization/{org_id}/dashboard_widgets/{id}/` - Delete widget

### 🔗 Shared Links

110. ✅ GET `/api/v1/organization/{org_id}/shared_links/` - List shared links
111. ✅ POST `/api/v1/organization/{org_id}/shared_links/` - Create shared link
112. ✅ GET `/api/v1/organization/{org_id}/shared_links/{id}/` - Get shared link
113. ✅ PUT `/api/v1/organization/{org_id}/shared_links/{id}/` - Update shared link
114. ✅ PATCH `/api/v1/organization/{org_id}/shared_links/{id}/` - Partial update shared link
115. ✅ DELETE `/api/v1/organization/{org_id}/shared_links/{id}/` - Delete shared link

### ⚙️ Configs

116. ✅ GET `/api/v1/organization/{org_id}/configs/` - List configs
117. ✅ POST `/api/v1/organization/{org_id}/configs/` - Create config
118. ✅ GET `/api/v1/organization/{org_id}/configs/{id}/` - Get config
119. ✅ PUT `/api/v1/organization/{org_id}/configs/{id}/` - Update config
120. ✅ PATCH `/api/v1/organization/{org_id}/configs/{id}/` - Partial update config
121. ✅ DELETE `/api/v1/organization/{org_id}/configs/{id}/` - Delete config

### 🤖 AI Reports

122. ✅ GET `/api/v1/organization/{org_id}/ai-reports/` - List AI reports
123. ✅ POST `/api/v1/organization/{org_id}/ai-reports/` - Create AI report
124. ✅ GET `/api/v1/organization/{org_id}/ai-reports/{id}/` - Get AI report
125. ✅ PUT `/api/v1/organization/{org_id}/ai-reports/{id}/` - Update AI report
126. ✅ PATCH `/api/v1/organization/{org_id}/ai-reports/{id}/` - Partial update AI report
127. ✅ DELETE `/api/v1/organization/{org_id}/ai-reports/{id}/` - Delete AI report
128. ✅ POST `/api/v1/organization/{org_id}/ai-reports/{id}/cancel/` - Cancel AI report

### 🔐 Personal Access Tokens

129. ✅ GET `/api/v1/organization/{org_id}/pat/` - List PATs
130. ✅ POST `/api/v1/organization/{org_id}/pat/` - Create PAT
131. ✅ GET `/api/v1/organization/{org_id}/pat/{id}/` - Get PAT
132. ✅ PUT `/api/v1/organization/{org_id}/pat/{id}/` - Update PAT
133. ✅ PATCH `/api/v1/organization/{org_id}/pat/{id}/` - Partial update PAT
134. ✅ DELETE `/api/v1/organization/{org_id}/pat/{id}/` - Delete PAT

### 📈 Forecasting

135. ✅ GET `/api/v1/forecasting/{project_id}/v3/` - Get forecast V3
136. ✅ GET `/api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/` - List forecast types
137. ✅ POST `/api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/` - Create forecast type
138. ✅ GET `/api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/{id}/` - Get forecast type
139. ✅ PUT `/api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/{id}/` - Update forecast type
140. ✅ PATCH `/api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/{id}/` - Partial update
141. ✅ DELETE `/api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/{id}/` - Delete
142. ✅ PATCH `/api/v1/organization/{org_id}/forecasting/item_types_for_forecasting/{id}/forecasting-properties/` - Update properties

### 💼 Capitalization

143. ✅ GET `/api/v1/organization/{org_id}/generate_capitalization/` - List cap reports
144. ✅ POST `/api/v1/organization/{org_id}/generate_capitalization/` - Generate cap report
145. ✅ GET `/api/v1/organization/{org_id}/generate_capitalization/{id}/` - Get cap report
146. ✅ GET `/api/v1/organization/{org_id}/generated_capitalization_reports/` - List generated reports
147. ✅ GET `/api/v1/organization/{org_id}/generated_capitalization_reports/{report_id}/` - Get report
148. ✅ DELETE `/api/v1/organization/{org_id}/generated_capitalization_reports/{report_id}/delete/` - Delete report
149. ✅ GET `/api/v1/organization/{org_id}/capitalization_reports/capitalization_report_config/` - Get config
150. ✅ POST `/api/v1/organization/{org_id}/capitalization_reports/capitalization_report_config/` - Create config
151. ✅ POST `/api/v1/organization/{org_id}/capitalization_reports/upload/` - Upload cap report
152. ✅ POST `/api/v1/organization/{org_id}/send_v2_cap_report/` - Send V2 cap report

### 📮 Subscriptions & Notifications

153. ✅ POST `/api/v1/organization/{org_id}/send_dashboard_subscriptions/` - Send dashboard subscriptions
154. ✅ POST `/api/v1/organization/{org_id}/apply_promo_code` - Apply promo code
155. ✅ POST `/api/v1/organization/{org_id}/change_company_setting/` - Change company setting

### 🗂️ Slots

156. ✅ GET `/api/v1/organization/{org_id}/slots/` - Get org slots
157. ✅ POST `/api/v1/organization/{org_id}/slots/create/` - Create slot
158. ✅ DELETE `/api/v1/organization/{org_id}/slots/create/` - Delete slot
159. ✅ GET `/api/v1/organization/{org_id}/slots/{slot_type}/` - Get slot by type
160. ✅ POST `/api/v1/organization/{org_id}/slots/{slot_type}/` - Update slot
161. ✅ DELETE `/api/v1/organization/{org_id}/slots/{slot_type}/` - Delete slots by type
162. ✅ POST `/api/v1/organization/{org_id}/slots/{slot_type}/config/copy-to-all/` - Copy config to all
163. ✅ POST `/api/v1/organization/{org_id}/projects/{project_id}/slots/{slot_type}/config/` - Update project slot config

### 📋 Error Logs

164. ✅ GET `/api/v1/organization/{org_id}/error_logs/` - Get error logs
165. ✅ DELETE `/api/v1/organization/{org_id}/error_logs/` - Clear error logs

### 🎯 Projects

166. ✅ GET `/api/v1/project/` - List all projects
167. ✅ GET `/api/v1/project/{project_id}/` - Get project
168. ✅ PUT `/api/v1/project/{project_id}/` - Update project
169. ✅ PATCH `/api/v1/project/{project_id}/` - Partial update project
170. ✅ POST `/api/v1/project/{project_id}/update` - Update project (alternate)
171. ✅ DELETE `/api/v1/project/{project_id}/delete` - Delete project
172. ✅ GET `/api/v1/project/{project_id}/service/` - List project services
173. ✅ GET `/api/v1/project/{project_id}/service/{id}/` - Get project service
174. ✅ GET `/api/v1/project/{project_id}/data_ingest_date/` - Get data ingest date
175. ✅ GET `/api/v1/project/{project_id}/configuration_options/` - Get config options
176. ✅ GET `/api/v1/project/{project_id}/item_props/` - Get item props
177. ✅ GET `/api/v1/project/{project_id}/item_props/{item_type}/` - Get item props by type
178. ✅ GET `/api/v1/project/{project_id}/enabled_users_count/` - Get enabled users count
179. ✅ POST `/api/v1/project/{project_id}/enable_disable_users/` - Enable/disable users
180. ✅ GET `/api/v1/project/{project_id}/get_service_links` - Get service links
181. ✅ POST `/api/v1/project/{project_id}/service_link` - Create service link
182. ✅ DELETE `/api/v1/project/{project_id}/service_link` - Delete service link

### 📊 Project Dashboards

183. ✅ GET `/api/v1/project/{project_id}/dashboards/` - List project dashboards
184. ✅ POST `/api/v1/project/{project_id}/dashboards/` - Create project dashboard
185. ✅ GET `/api/v1/project/{project_id}/dashboards/names/` - Get dashboard names
186. ✅ GET `/api/v1/project/{project_id}/dashboards/{id}/` - Get dashboard
187. ✅ PUT `/api/v1/project/{project_id}/dashboards/{id}/` - Update dashboard
188. ✅ PATCH `/api/v1/project/{project_id}/dashboards/{id}/` - Partial update dashboard
189. ✅ DELETE `/api/v1/project/{project_id}/dashboards/{id}/` - Delete dashboard
190. ✅ DELETE `/api/v1/project/{project_id}/dashboards/{id}/clear_widgets/` - Clear widgets
191. ✅ POST `/api/v1/project/{project_id}/dashboards/{id}/copy/` - Copy dashboard
192. ✅ GET `/api/v1/project/{project_id}/dashboard_widgets/` - List widgets
193. ✅ POST `/api/v1/project/{project_id}/dashboard_widgets/` - Create widget
194. ✅ POST `/api/v1/project/{project_id}/dashboard_widgets/multidash/` - Create multi-dash
195. ✅ GET `/api/v1/project/{project_id}/dashboard_widgets/{id}/` - Get widget
196. ✅ PUT `/api/v1/project/{project_id}/dashboard_widgets/{id}/` - Update widget
197. ✅ PATCH `/api/v1/project/{project_id}/dashboard_widgets/{id}/` - Partial update widget
198. ✅ DELETE `/api/v1/project/{project_id}/dashboard_widgets/{id}/` - Delete widget
199. ✅ GET `/api/v1/project/{project_id}/dashboard_subscriptions` - Get subscriptions
200. ✅ POST `/api/v1/project/{project_id}/dashboard_subscriptions` - Create subscription

### 🎯 Project Service Users

201. ✅ GET `/api/v1/project/{project_id}/service_user/` - List project service users
202. ✅ GET `/api/v1/project/{project_id}/tag` - List project tags
203. ✅ GET `/api/v1/project/{project_id}/tag/{tag_id}` - Get tag
204. ✅ POST `/api/v1/project/{project_id}/tag/{tag_id}` - Add/update tag
205. ✅ DELETE `/api/v1/project/{project_id}/tag/{tag_id}` - Remove tag

### 🚨 Risk Management

206. ✅ GET `/api/v1/project/{project_id}/risk_definitions/` - List risk definitions
207. ✅ POST `/api/v1/project/{project_id}/risk_definitions/` - Create risk definition
208. ✅ GET `/api/v1/project/{project_id}/risk_definitions/{id}/` - Get risk definition
209. ✅ PUT `/api/v1/project/{project_id}/risk_definitions/{id}/` - Update risk definition
210. ✅ PATCH `/api/v1/project/{project_id}/risk_definitions/{id}/` - Partial update
211. ✅ DELETE `/api/v1/project/{project_id}/risk_definitions/{id}/` - Delete risk definition
212. ✅ GET `/api/v1/project/{project_id}/risk_notify_options` - Get risk notify options
213. ✅ GET `/api/v1/project/{project_id}/risks/service_items/types/` - Get risk item types
214. ✅ GET `/api/v1/project/{project_id}/alert_subscriptions/` - Get alert subscriptions
215. ✅ PATCH `/api/v1/project/{project_id}/alert_subscriptions/` - Update alert subscriptions

### 📝 Project Settings

216. ✅ GET `/api/v1/project/{project_id}/autopin_message/` - Get autopin message
217. ✅ PUT `/api/v1/project/{project_id}/autopin_message/` - Update autopin message
218. ✅ PATCH `/api/v1/project/{project_id}/autopin_message/` - Partial update autopin
219. ✅ GET `/api/v1/project/{project_id}/production_deploy_filter/` - Get deploy filter
220. ✅ PATCH `/api/v1/project/{project_id}/production_deploy_filter/` - Update deploy filter

### 📊 Filter Sets

221. ✅ GET `/api/v1/project/{project_id}/metrics_filter_sets/` - List filter sets
222. ✅ POST `/api/v1/project/{project_id}/metrics_filter_sets/` - Create filter set
223. ✅ GET `/api/v1/project/{project_id}/metrics_filter_sets/{id}/` - Get filter set
224. ✅ PUT `/api/v1/project/{project_id}/metrics_filter_sets/{id}/` - Update filter set
225. ✅ PATCH `/api/v1/project/{project_id}/metrics_filter_sets/{id}/` - Partial update
226. ✅ DELETE `/api/v1/project/{project_id}/metrics_filter_sets/{id}/` - Delete filter set

### 🎯 Milestones

227. ✅ GET `/api/v1/project/{project_id}/pinned_milestones` - Get pinned milestones
228. ✅ POST `/api/v1/project/{project_id}/pin_unpin_milestone/{item_id}` - Pin/unpin milestone
229. ✅ GET `/api/v1/project/{project_id}/milestone_custom_sort` - Get milestone sort
230. ✅ POST `/api/v1/project/{project_id}/milestone_custom_sort` - Update milestone sort
231. ✅ GET `/api/v1/project/{project_id}/enabled_portfolio_columns` - Get enabled columns
232. ✅ POST `/api/v1/project/{project_id}/enabled_portfolio_columns` - Update enabled columns
233. ✅ POST `/api/v1/project/{project_id}/dynamic_filter_set_milestone_data/` - Get dynamic filter data

### 💾 Saved Views

234. ✅ GET `/api/v1/project/{project_id}/saved_service_item_view/` - Get saved SI view
235. ✅ POST `/api/v1/project/{project_id}/saved_service_item_view/` - Create saved SI view
236. ✅ GET `/api/v1/project/{project_id}/saved_work_bundle_view/` - Get saved WB view
237. ✅ POST `/api/v1/project/{project_id}/saved_work_bundle_view/` - Create saved WB view
238. ✅ POST `/api/v1/project/{project_id}/pin_unpin_metric/{metric_id}/{view_name}` - Pin/unpin metric
239. ✅ DELETE `/api/v1/project/{project_id}/pin_unpin_metric/{metric_id}/{view_name}` - Delete pin

### 🌳 Visualization

240. ✅ GET `/api/v1/project/{project_id}/tree_visualization/` - Get tree visualization
241. ✅ GET `/api/v1/report/{project_id}/service_props/` - Get service properties

### 👔 Employee

242. ✅ GET `/api/v1/employee/{project_id}/metrics/` - Get employee metrics
243. ✅ GET `/api/v1/employee/{project_id}/periods/` - Get employee periods
244. ✅ GET `/api/v1/employee/{project_id}/users/` - Get employee users
245. ✅ GET `/api/v1/employee/{project_id}/{metric_id}/metric-data/` - Get employee metric data

### 🔄 Selectable Work Bundles (Organization)

246. ✅ GET `/api/v1/organization/{org_id}/service/{service_id}/selectable_work_bundles/` - List bundles
247. ✅ POST `/api/v1/organization/{org_id}/service/{service_id}/selectable_work_bundles/` - Save bundles
248. ✅ POST `/api/v1/organization/{org_id}/service/{service_id}/selectable_work_bundles/{work_bundle_id}/` - Update bundle
249. ✅ POST `/api/v1/organization/{org_id}/service/{service_id}/selectable_work_bundles/{work_bundle_id}/toggle_children/` - Toggle children
250. ✅ POST `/api/v1/organization/{org_id}/service/{service_id}/toggle_all_selectable_work_bundles/` - Toggle all

### 🔄 Selectable Work Bundles (Project)

251. ✅ GET `/api/v1/project/{project_id}/service/{service_id}/selectable_work_bundles/` - List bundles
252. ✅ POST `/api/v1/project/{project_id}/service/{service_id}/selectable_work_bundles/` - Save bundles
253. ✅ POST `/api/v1/project/{project_id}/service/{service_id}/selectable_work_bundles/{work_bundle_id}/` - Update bundle
254. ✅ POST `/api/v1/project/{project_id}/service/{service_id}/selectable_work_bundles/{work_bundle_id}/toggle_children/` - Toggle children
255. ✅ POST `/api/v1/project/{project_id}/service/{service_id}/toggle_all_selectable_work_bundles/` - Toggle all

### 🗂️ Project Slots

256. ✅ GET `/api/v1/project/{project_id}/slots/` - Get project slots
257. ✅ GET `/api/v1/project/{project_id}/slots/{slot_type}/` - Get slot by type
258. ✅ POST `/api/v1/project/{project_id}/slots/{slot_type}/` - Update slot
259. ✅ GET `/api/v1/project/{project_id}/templates/` - Get templates

### 📊 Charts & Analysis

260. ✅ POST `/api/v1/charts/analysis/` - Create chart analysis
261. ✅ POST `/api/v1/charts/analyze` - Analyze chart

### 🤖 Action AI

262. ✅ POST `/api/v1/project/{project_id}/actionai/ai-metric-builder/` - AI metric builder
263. ✅ POST `/api/v1/project/{project_id}/actionai/code-query/` - Code query
264. ✅ POST `/api/v1/project/{project_id}/actionai/code-query-json/` - Code query JSON
265. ✅ GET `/api/v1/project/{project_id}/ai_auth_token/` - Get AI auth token
266. ✅ POST `/api/v1/project/{project_id}/ai_auth_token/` - Save AI auth token

### ☁️ External AI Services

267. ✅ POST `/api/v1/project/{project_id}/cursor_usage_data/` - Get Cursor usage
268. ✅ POST `/api/v1/project/{project_id}/cursor_usage_data_with_token/` - Get Cursor usage with token
269. ✅ GET `/api/v1/project/{project_id}/q_usage_config/` - Get Q usage config
270. ✅ POST `/api/v1/project/{project_id}/q_usage_config/` - Save Q usage config
271. ✅ POST `/api/v1/project/{project_id}/q_usage_data/` - Get Q usage data

### 🌐 Population Benchmarks

272. ✅ GET `/api/v1/population-benchmarks/metric/{metric_type}` - Get population benchmark

### 👤 User Endpoints

273. ✅ POST `/api/v1/user/favorite_workspace/` - Add/remove favorite workspace
274. ✅ DELETE `/api/v1/user/favorite_workspace/` - Delete favorite
275. ✅ GET `/api/v1/user/get_organization/` - Get user organization
276. ✅ POST `/api/v1/user/save_welcome_info/` - Save welcome info

### 🔧 Utility

277. ✅ GET `/api/v1/utility/generate_rsa_key_pair` - Generate RSA key pair

### 💬 Slack Integration (Survey/DX)

278. ✅ GET `/api/v1/slack_integration/organization/{org_id}/survey/` - Get surveys
279. ✅ POST `/api/v1/slack_integration/organization/{org_id}/survey/` - Create survey
280. ✅ POST `/api/v1/slack_integration/survey/organization/{org_id}/` - Send survey batch
281. ✅ GET `/api/v1/slack_integration/organization/{company_id}/survey/service_items/` - Get survey items
282. ✅ GET `/api/v1/slack_integration/organization/{org_id}/survey/themes/` - Get survey themes
283. ✅ POST `/api/v1/slack_integration/organization/{org_id}/survey/themes/` - Create theme
284. ✅ GET `/api/v1/slack_integration/organization/{org_id}/survey/total_responses/` - Get total responses
285. ✅ GET `/api/v1/slack_integration/project/{project_id}/notification_preference_options/` - Get notif preferences
286. ✅ POST `/api/v1/slack_integration/interactive/` - Handle Slack interactive
287. ✅ POST `/api/v1/slack_integration/survey/` - Create survey

### 🎨 Service Issue States

288. ✅ GET `/api/v1/project/{project_id}/service_issue_states/` - Get issue states

---

## Total: ~288 Non-Admin, Non-Destructive Endpoints to Implement

### Exclusions (Admin/Destructive):
- All `/api/v1/iadmin/*` endpoints (admin only)
- DELETE organization endpoints
- DELETE service endpoints (most)
- DELETE project service link (included as it's reversible)


