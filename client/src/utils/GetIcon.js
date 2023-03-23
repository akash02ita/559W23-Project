import { Folder,  FileEarmarkImage, FiletypeTxt, FileEarmarkPdf, FiletypeMp4} from "react-bootstrap-icons";

function GetIcon({ fname, size }) {
    console.log("utils: getFileIcon: fname is ", fname);
    const arr = fname.split('.');
    if (arr.length == 1) {
        console.log("utils: getFileIcon: failed: array length is 1");
        return <></>;
    }

    const ext = arr[arr.length-1]; // file extension
    switch(ext) {
        case 'jpg':
            return size ? <FileEarmarkImage size={size}/> : <FileEarmarkImage />;
            break;
        case 'png':
            return size ? <FileEarmarkImage size={size}/> : <FileEarmarkImage />;
            break;
        case 'txt':
            return size ? <FiletypeTxt size={size}/> : <FiletypeTxt />;
            break;
        case 'mp4':
            return size ? <FiletypeMp4 size={size}/> : <FiletypeMp4 />;
            break;
        case 'jpeg':
            return size ? <FileEarmarkImage size={size}/> : <FileEarmarkImage />;
            break;
        case 'pdf':
            return size ? <FileEarmarkPdf size={size}/> : <FileEarmarkPdf />;
            break;
        default:
            console.log("utils: getFileIcon: failed: default no icon for extension", ext);
            return <></>
    }
}

export default GetIcon;
