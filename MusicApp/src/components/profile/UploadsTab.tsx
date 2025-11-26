import OptionsModal from '@components/OptionsModal';
import AudioListItem from '@ui/AudioListItem';
import AudioListLoadingUI from '@ui/AudioListLoadingUI';
import EmptyRecords from '@ui/EmptyRecords';
import {FC, useState} from 'react';
import {StyleSheet, ScrollView, Pressable, Text} from 'react-native';
import {useSelector} from 'react-redux';
import {AudioData} from 'src/@types/audio';
import {useFetchUploadsByProfile} from 'src/hooks/query';
import useAudioController from 'src/hooks/useAudioController';
import {getPlayerState} from 'src/store/player';
import AntiDesign from 'react-native-vector-icons/AntDesign';
import colors from '@utils/colors';
import {NavigationProp, useNavigation} from '@react-navigation/native';
import {ProfileNavigatorStackParamList} from 'navigation';

interface Props {}

const UploadsTab: FC<Props> = props => {
  const [showOptions, setShowOptions] = useState(false);
  const [selectedAudio, setSelectedAudio] = useState<AudioData>();

  const {onGoingAudio} = useSelector(getPlayerState);
  const {data, isLoading} = useFetchUploadsByProfile();
  const {onAudioPress} = useAudioController();
  const {navigate} =
    useNavigation<NavigationProp<ProfileNavigatorStackParamList>>();

  const handleOnLongPress = (audio: AudioData) => {
    setSelectedAudio(audio);
    setShowOptions(true);
  };

  const handleOnEditPress = () => {
    setShowOptions(false);
    if (selectedAudio )
      navigate('UpdateAudio', {
        audio: selectedAudio,
      });
  };

  if (isLoading) return <AudioListLoadingUI />;

  if (!data?.length) return <EmptyRecords title="There is no audio!" />;

  return (
    <>
      <ScrollView style={styles.container}>
        {data?.map(item => {
          return (
            <AudioListItem
              onPress={() => onAudioPress(item, data)}
              key={item.id}
              audio={item}
              isPlaying={onGoingAudio?.id === item.id}
              onLongPress={() => handleOnLongPress(item)}
            />
          );
        })}
      </ScrollView>
      <OptionsModal
        visible={showOptions}
        onRequestClose={() => {
          setShowOptions(false);
        }}
        options={[
          {
            title: 'Edit',
            icon: 'edit',
            onPress: handleOnEditPress,
          },
        ]}
        renderItem={item => {
          return (
            <Pressable onPress={item.onPress} style={styles.optionContainer}>
              <AntiDesign size={24} color={colors.PRIMARY} name={item.icon} />
              <Text style={styles.optionLabel}>{item.title}</Text>
            </Pressable>
          );
        }}
      />
    </>
  );
};

const styles = StyleSheet.create({
  container: {},
  optionContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
  },
  optionLabel: {color: colors.PRIMARY, fontSize: 16, marginLeft: 5},
});

export default UploadsTab;


// import AudioForm from '@components/form/AudioForm';
// import {NativeStackScreenProps} from '@react-navigation/native-stack';
// import {mapRange} from '@utils/math';
// import {FC, useState} from 'react';
// import {StyleSheet} from 'react-native';
// import {useQueryClient} from 'react-query';
// import {useDispatch} from 'react-redux';
// import {ProfileNavigatorStackParamList} from 'src/@types/navigation';
// import catchAsyncError from 'src/api/catchError';
// import {getClient} from 'src/api/client';
// import {upldateNotification} from 'src/store/notification';

// type Props = NativeStackScreenProps<
//   ProfileNavigatorStackParamList,
//   'UpdateAudio'
// >;

// const UpdateAudio: FC<Props> = (props) => {
//   const {audio} = props.route.params;
//   const [uploadProgress, setUploadProgress] = useState(0);
//   const [busy, setBusy] = useState(false);

//   const queryClient = useQueryClient();
//   const dispatch = useDispatch();

//   const handleUpdate = async (formdata: FormData) => {
//     setBusy(true);
//     try {
//       const client = await getClient({'Content-Type': 'multipart/form-data;'});

//       const {data} = await client.patch('/audio/' + audio.id, formdata, {
//         onUploadProgress(progressEvent) {
//           const uploaded = mapRange({
//             inputMin: 0,
//             inputMax: progressEvent.total || 0,
//             outputMin: 0,
//             outputMax: 100,
//             inputValue: progressEvent.loaded,
//           });

//           if (uploaded >= 100) {
//             setBusy(false);
//           }

//           setUploadProgress(Math.floor(uploaded));
//         },
//       });

//       queryClient.invalidateQueries({queryKey: ['upload-by-profile']});
//     } catch (error) {
//       const errorMessage = catchAsyncError(error);
//       dispatch(upldateNotification({message: errorMessage, type: 'error'}));
//     }
//     setBusy(false);
//   };

//   return (
//     <AudioForm
//       initialValues={{
//         title: audio.title,
//         category: audio.category,
//         about: audio.about,
//       }}
//       onSubmit={handleUpdate}
//       busy={busy}
//       progress={uploadProgress}
//     />
//   );
// };

// const styles = StyleSheet.create({
//   container: {},
// });

// export default UpdateAudio;
