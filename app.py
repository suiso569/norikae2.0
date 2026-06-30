import streamlit as st
import networkx as nx

# ==========================================
# 1. 路線・駅名・施設データ
# ==========================================
def get_station_kana():
    return {
        "一ノ瀬": "いちのせ", "境港": "さかいみなと", "谷上町": "たにかみちょう", "第1拠点": "だいいちきょてん",
        "晴海坂": "はるみざか", "滝沢": "たきさわ", "終宮": "ついのみや", "新蒼海宮": "しんそうかいぐう",
        "蒼海宮": "そうかいぐう", "荒山村": "あらやまむら", "桜町一丁目": "さくらまちいっちょうめ",
        "谷上三丁目": "たにかみさんちょうめ", "白浜崎": "しらはまざき", "砂炭江": "さずみえ",
        "霧ヶ峰": "きりがみね", "霧ヶ峰湖": "きりがみねこ", "風見野": "かざみの",
        "北茜ヶ原": "きたあかねがはら", "茜ヶ原": "あかねがはら", "桜坂": "さくらざか",
        "緑山": "みどりやま", "旭ヶ丘": "あさひがおか", "亀浜": "かめはま", "西霧ヶ峰": "にしきりがみね",
        "新都町": "しんみやこまち", "前哨基地": "ぜんしょうきち", "朝凪": "あさなぎ",
        "速見": "はやみ", "南新都町": "みなみしんみやこまち", "朝凪南": "あさなぎみなみ",
        "東晴海坂": "ひがしはるみざか"
    }

def get_facilities():
    return {
        "一ノ瀬": "たかのり拠点",
        "境港": "ブランチマイニング場",
        "谷上町": "初拠点付近",
        "桜町一丁目": "初期スポーン地点最寄り",
        "荒山村": "村人交易所",
        "東晴海坂": "天空トラップ",
        "終宮": "エンドポータル最寄り駅",
        "新蒼海宮": "吉岡拠点※予定",
        "蒼海宮": "ガーディアントラップ",
        "亀浜": "霧ヶ峰空港, 竹製造機, 第二拠点中心部",
        "霧ヶ峰": "羊毛製造機",
        "霧ヶ峰湖": "畑, 牧場",
        "茜ヶ原": "メサ最寄り駅",
        "前哨基地": "前哨基地最寄り駅",
        "朝凪": "第3拠点周辺"
    }

LINES_STATIONS = {
    "中央線": ["一ノ瀬", "境港", "谷上町", "第1拠点", "晴海坂", "滝沢", "終宮", "新蒼海宮", "蒼海宮"],
    "桜町線(各停)": ["荒山村", "桜町一丁目", "谷上三丁目", "白浜崎", "砂炭江", "霧ヶ峰", "霧ヶ峰湖", "風見野", "北茜ヶ原", "茜ヶ原"],
    "桜町線(快速)": ["白浜崎", "霧ヶ峰", "茜ヶ原"],
    "東西線": ["一ノ瀬", "桜坂", "緑山", "旭ヶ丘", "霧ヶ峰", "亀浜"],
    "南北線": ["西霧ヶ峰", "新都町", "前哨基地"],
    "霧ヶ峰線": ["蒼海宮", "亀浜", "西霧ヶ峰", "霧ヶ峰湖"],
    "新都心線": ["終宮", "亀浜", "新都町", "朝凪"],
    "中央都市線": ["速見", "霧ヶ峰", "西霧ヶ峰", "南新都町", "朝凪南", "朝凪"],
    "南辺線": ["風見野", "前哨基地"],
    "中央新幹線": ["白浜崎", "新蒼海宮"],
    "晴海坂線": ["砂炭江", "晴海坂", "東晴海坂"]
}

def get_lines_data():
    return {
        "中央線": [("一ノ瀬", "境港", 120), ("境港", "谷上町", 60), ("谷上町", "第1拠点", 30), ("第1拠点", "晴海坂", 30), ("晴海坂", "滝沢", 90), ("滝沢", "終宮", 120), ("終宮", "新蒼海宮", 120), ("新蒼海宮", "蒼海宮", 60)],
        "桜町線(各停)": [("荒山村", "桜町一丁目", 60), ("桜町一丁目", "谷上三丁目", 30), ("谷上三丁目", "白浜崎", 60), ("白浜崎", "砂炭江", 90), ("砂炭江", "霧ヶ峰", 90), ("霧ヶ峰", "霧ヶ峰湖", 60), ("霧ヶ峰湖", "風見野", 120), ("風見野", "北茜ヶ原", 120), ("北茜ヶ原", "茜ヶ原", 60)],
        "桜町線(快速)": [("白浜崎", "霧ヶ峰", 120), ("霧ヶ峰", "茜ヶ原", 240)],
        "東西線": [("一ノ瀬", "桜坂", 180), ("桜坂", "緑山", 180), ("緑山", "旭ヶ丘", 60), ("旭ヶ丘", "霧ヶ峰", 90), ("霧ヶ峰", "亀浜", 60)],
        "南北線": [("西霧ヶ峰", "新都町", 30), ("新都町", "前哨基地", 180)],
        "霧ヶ峰線": [("蒼海宮", "亀浜", 150), ("亀浜", "西霧ヶ峰", 30), ("西霧ヶ峰", "霧ヶ峰湖", 60)],
        "新都心線": [("終宮", "亀浜", 130), ("亀浜", "新都町", 60), ("新都町", "朝凪", 60)],
        "中央都市線": [("速見", "霧ヶ峰", 60), ("霧ヶ峰", "西霧ヶ峰", 30), ("西霧ヶ峰", "南新都町", 60), ("南新都町", "朝凪南", 60), ("朝凪南", "朝凪", 60)],
        "南辺線": [("風見野", "前哨基地", 150)],
        "中央新幹線": [("白浜崎", "新蒼海宮", 50)],
        "晴海坂線": [("砂炭江", "晴海坂", 120), ("晴海坂", "東晴海坂", 60)]
    }

def get_direction(line_name, from_station, to_station):
    if line_name in LINES_STATIONS:
        stations = LINES_STATIONS[line_name]
        if from_station in stations and to_station in stations:
            idx_from = stations.index(from_station)
            idx_to = stations.index(to_station)
            return f"{stations[-1]}行" if idx_to > idx_from else f"{stations[0]}行"
    return ""

# ==========================================
# 2. グラフ構築
# ==========================================
@st.cache_resource
def build_graph():
    G = nx.Graph()
    lines = get_lines_data()
    station_lines = {}
    
    for line_name, edges in lines.items():
        for u, v, w in edges:
            # weightは計算用として残す
            G.add_edge(f"{u}|{line_name}", f"{v}|{line_name}", weight=w, line=line_name, is_transfer=False)
            station_lines.setdefault(u, set()).add(line_name)
            station_lines.setdefault(v, set()).add(line_name)
            
    for sta, slines in station_lines.items():
        sorted_slines = sorted(list(slines))
        for i in range(len(sorted_slines)):
            for j in range(i+1, len(sorted_slines)):
                G.add_edge(f"{sta}|{sorted_slines[i]}", f"{sta}|{sorted_slines[j]}", weight=30, line="🔄 乗り換え", is_transfer=True)
    
    return G, station_lines

# ==========================================
# 3. UIメイン処理
# ==========================================
def main():
    st.set_page_config(page_title="Minecraft鉄道 乗り換え案内", layout="centered")
    st.title("Minecraft鉄道 乗り換え案内 🛤️")
    
    G_base, station_lines = build_graph()
    station_kana = get_station_kana()
    facilities = get_facilities()
    
    # 駅リストの五十音順ソートと、施設名の結合
    sorted_stations = sorted(list(station_lines.keys()), key=lambda x: station_kana[x])
    station_options = []
    for s in sorted_stations:
        base_name = f"{s} ({station_kana[s]})"
        if s in facilities:
            station_options.append(f"{base_name} 🏕️ {facilities[s]}")
        else:
            station_options.append(base_name)

    st.markdown("### 出発・到着駅を選択")
    col1, col2 = st.columns(2)
    # デフォルトを荒山村と霧ヶ峰に設定
    default_start = [opt for opt in station_options if opt.startswith("荒山村")][0] if any(opt.startswith("荒山村") for opt in station_options) else station_options[0]
    default_end = [opt for opt in station_options if opt.startswith("霧ヶ峰 ")][0] if any(opt.startswith("霧ヶ峰 ") for opt in station_options) else station_options[1]
    
    start_str = col1.selectbox("出発駅", station_options, index=station_options.index(default_start))
    end_str = col2.selectbox("到着駅", station_options, index=station_options.index(default_end))
    
    start_sta = start_str.split(' ')[0]
    end_sta = end_str.split(' ')[0]

    if st.button("経路を検索", type="primary", use_container_width=True):
        if start_sta == end_sta:
            st.warning("出発駅と到着駅が同じです。")
            return

        G = G_base.copy()
        for line in station_lines[start_sta]:
            G.add_edge("START", f"{start_sta}|{line}", weight=0, line="乗車", is_transfer=False)
        for line in station_lines[end_sta]:
            G.add_edge(f"{end_sta}|{line}", "END", weight=0, line="降車", is_transfer=False)

        try:
            path = nx.shortest_path(G, "START", "END", weight="weight")
            
            steps = []
            transfer_count = 0
            actual_path = path[1:-1]

            for i in range(len(actual_path)-1):
                u, v = actual_path[i], actual_path[i+1]
                data = G.get_edge_data(u, v)
                u_sta = u.split('|')[0]
                v_sta = v.split('|')[0]
                
                if data['is_transfer']:
                    transfer_count += 1
                
                if steps and not data['is_transfer'] and steps[-1]['line'] == data['line']:
                    steps[-1]['to'] = v_sta
                    steps[-1]['intermediates'].append(u_sta)
                else:
                    steps.append({
                        "from": u_sta, "to": v_sta, "line": data['line'], 
                        "is_transfer": data['is_transfer'], "intermediates": []
                    })
            
            # 時間表示を削除し、乗換回数のみ表示
            st.success(f"🔄 乗換: **{transfer_count}回**")
            st.divider()
            
            for step in steps:
                if step['is_transfer']:
                    # 乗り換え時間も非表示に
                    st.markdown(f"<div style='text-align: center; color: gray; margin: 10px 0;'>↑↓ {step['from']}駅で乗り換え</div>", unsafe_allow_html=True)
                else:
                    with st.container(border=True):
                        from_fac = f" 🏕️ {facilities[step['from']]}" if step['from'] in facilities else ""
                        st.markdown(f"### 🚉 {step['from']}{from_fac}")
                        
                        direction = get_direction(step['line'], step['from'], step['to'])
                        dir_str = f" [ {direction} ]" if direction else ""
                        
                        # 乗車時間も非表示に
                        st.markdown(f"**⬇ 🚆 {step['line']}**{dir_str}")
                        
                        if step['intermediates']:
                            with st.expander(f"🔽 途中駅（{len(step['intermediates'])}駅）"):
                                for inter in step['intermediates']:
                                    st.write(f" ・ {inter}")
                                    
                        to_fac = f" 🏕️ {facilities[step['to']]}" if step['to'] in facilities else ""
                        st.markdown(f"### 🏁 {step['to']}{to_fac}")

        except nx.NetworkXNoPath:
            st.error("経路が見つかりませんでした。")

    st.divider()
    
    st.markdown("### 🏕️ 施設・拠点から駅を探す")
    with st.expander("主要施設・拠点一覧を表示"):
        for sta in sorted_stations:
            if sta in facilities:
                st.markdown(f"- **{sta}駅** ({station_kana[sta]}) …… {facilities[sta]}")
                
    st.divider()

    st.markdown("### 🚉 駅の接続路線を調べる")
    selected_str = st.selectbox("駅を選択", station_options, key="station_info")
    target_sta = selected_str.split(' ')[0]
    
    if target_sta in station_lines:
        lines = sorted(list(station_lines[target_sta]))
        with st.container(border=True):
            st.markdown(f"**{target_sta}駅 ({station_kana[target_sta]})** の接続路線")
            for line in lines:
                st.markdown(f"- 🚆 {line}")

if __name__ == "__main__":
    main()